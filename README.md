# Background
Most of the functions, methods and classes leveraged in this repo rely on the [dl-rom](https://github.com/NicolaRFranco/dlroms) code and on the [PySINDy](https://github.com/dynamicslab/pysindy) library for the model discovery section

# POD-Galerking RB method
This method, in a nutshell, consists of the following maps combinations. Where $\Psi(\mu)$ is the parametrised solution map of the considered PDE, $\mu \in \mathcal{P} \subset \mathbb{R}^p$ the parameter vector, $s$ is the output of the associated functional (for instance, the velocity field in 2D has two components, therefore $s=2$), $V$ being an Hilbert-space

$$
\begin{align}
\Psi(\mu):\mathcal{P}\rightarrow V\\
s: V \rightarrow \mathbb{R}^s
\end{align}
$$

Hence the overall FOM (full order model) pipeline would be

$$s\circ \Psi(\mu): \mathcal{P}\rightarrow V \rightarrow \mathbb{R}^s$$

But, the idea is to employ a different space $V$ that will be the reduced one, i.e. the low-dimensional space $V_N \subset V$. Now the former pipeline becomes

$$s \circ \Psi(\mu)_N : \mathcal{P} \rightarrow V_N \rightarrow \mathbb{R}^s $$

where $\Psi(\mu)_N \in V_N$.
## Parametrized Shcrodinger's Equation
$$
\begin{equation}
    \begin{cases}
    ih\frac{\partial \psi}{\partial t}=-\frac{\hbar}{2m}\nabla \psi + V_{\mu}\psi &\quad on \thinspace\Omega\times (0,T)\\
    \psi_{\mathbb{R}}(t,x)=0 &\quad in \thinspace \partial \Omega\\
    \psi_{\mathbb{C}}(t,x)=0 &\quad in \thinspace \partial \Omega\\
    \psi_{\mathbb{R}}(0,x)=e^{-100||x||^2} &\quad in \thinspace \Omega, t=0 \\
    \psi_{\mathbb{C}}(0,x)=0 &\quad in \thinspace \Omega, t=0\\
\end{cases}
\end{equation}
$$

The affine decomposition of the problem is

$$  V_{\mu} =Ex_1+\Delta V \mathbf{1}_{(0,+\infty)}x_2 $$
+ Now the FEM solution of this model, which is a diffusion-reaction equation, is repeated for different (random) parameters to build the $\mathcal{M}_h$ space linked to the
   so-called snapshot matrix, upon which the POD decomposition is performed.
+ We get the functions needed to build the reduced model of the S.E.,  since the entire problem is projected in another space endowed with some special properties, it has been
  possible to achieve a tremendous reduction (x100/x200) in the time needed to perform the same simulation.

## Multiphysics: Stokes + Diffusion/Transport (chemical species)
...  READ-ME in progress
