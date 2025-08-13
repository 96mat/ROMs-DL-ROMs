from dlroms import*
import numpy as np

from dlroms.dnns import Weightless
from torch import matmul
ntimes=41
latent=9

class Library(Weightless):
  def __init__(self, lib):
    super(Library, self).__init__()
    self.lib = lib

  def forward(self, x):
    from torch import cat
    nx = len(x)
    return cat([f(x).reshape(nx, -1) for f in self.lib], axis = -1)

class SINDy(ROM):
  def __init__(self, *args, **kwargs):
    from torch.nn import Parameter
    super(SINDy, self).__init__(*args, **kwargs)
    self.thr = Parameter(dv.tensor(0.0))

  def threshold(self, A0):
    # Hard-promotes sparsity by clamping values close to 0 (with a learnable threshold)
    return relu(A0-self.thr) - relu(-A0-self.thr)

  def A(self, mu):
    eta = self[0]
    A0 = eta(mu)
    return self.threshold(A0)

  def forward(self, mu, z):
    A = self.A(mu)
    theta = self.Xi(z).unsqueeze(-1)
    return matmul(A, theta).squeeze(-1), A

  def freeze(self, *args, **kwargs):
    super(SINDy, self).freeze(*args, **kwargs)
    self.thr.requires_grad_(False)

  def unfreeze(self, *args, **kwargs):
    super(SINDy, self).freeze(*args, **kwargs)
    self.thr.requires_grad_(True)

  def evolve(self, mu0, z0, steps, tau):
    from torch import atleast_2d
    mu0s = atleast_2d(mu0)
    z0s = atleast_2d(z0)

    many, n = z0s.shape
    zsindy = self.coretype().zeros(many, steps + 1, n)
    zsindy[:, 0] = z0s
    for j in range(steps):
      dzdtj = self.forward(mu0s, zsindy[:, j])[0]
      zsindy[:, j+1] = zsindy[:, j] + tau*dzdtj

    return zsindy

  def parameters(self, *args, **kwargs):
    return super(SINDy, self).parameters() + [self.thr]

  def He(self, *args, **kwargs):
    from torch.nn import Parameter
    super(SINDy, self).He(*args, **kwargs)
    self.thr = Parameter(dv.tensor(0.0))


def dt(zval):
  """Approximation of time derivatives via finite differences.
  Later used in the definition of the loss to approximate the true derivatives."""
  tau = 5e-6
  zprev = zval.reshape(-1, ntimes, latent)[:, :-2, :].reshape(-1, latent)
  znext = zval.reshape(-1, ntimes, latent)[:, 2: ,  :].reshape(-1, latent) ### <--- latent state at time instant "i+1", for each sample in the batch
  dzdt = (znext-zprev)/(2*tau)
  return dzdt


from torch.optim import Adam
def sindy_loss(ztrue, sindy_output):
  dzpred, A = sindy_output
  dzdt_true = dt(ztrue) ### <-- time derivatives of the true latent coordinates
  return mse(euclidean)(dzdt_true, dzpred.reshape(-1, ntimes, latent)[:, 1:-1].reshape(-1, latent)) + 1e-4*A.abs().tanh().sum(axis = -1).sum(axis = -1).mean() # promotes sparsity via l1-penalty

def sindy_error(ztrue, sindy_output):
  dzpred, A = sindy_output
  dzdt_true = dt(ztrue) ### <-- time derivatives of the true latent coordinates
  return mse(euclidean)(dzdt_true, dzpred.reshape(-1, ntimes, latent)[:, 1:-1].reshape(-1, latent))