# Background
Most of the functions, methods and classes leveraged in this repo rely on the [dl-rom](https://github.com/NicolaRFranco/dlroms) code and on the [PySINDy](https://github.com/dynamicslab/pysindy) library for the model discovery section.

+ In order to run the ```PySINDy``` library and the relative examples, install its [latest version](https://pypi.org/project/pysindy/):
  ```
  pip install pysindy==2.0.0rc3
  ```
+ Sampling snapshots employing the [Latin-Hypercube](https://pythonhosted.org/pyDOE/randomized.html) nearly-randomized paradigm:
  ```
  !pip install pyDOE
  ```
+ Parallelise *tasks* by pickling *workers* created in [Ray](https://docs.ray.io/en/latest/index.html):
  ```
  !pip install -q ray
  !pip install -U "ray[default]"
  ```
# POD-Galerkin RB method
This method, in a nutshell, consists of the following map combinations [[1]](https://arxiv.org/abs/1511.02021). Where $\Psi(\mu)$ is the parametrised solution map of the considered PDE, $\mu \in \mathcal{P} \subset \mathbb{R}^p$ the parameter vector, $s$ is the output of the associated functional (for instance, the velocity field in 2D has two components, therefore $s=2$), $V$ being an Hilbert-space

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
+ Now the FEM solution of this model, which is a diffusion-reaction equation, is repeated for different (random) parameters to build the $\mathcal{M}\subset V_h$ subset linked to the
   so-called snapshot matrix, upon which the POD decomposition is performed.
+ We get the functions needed to build the reduced model of the S.E.,  since the entire problem is projected in another space endowed with some special properties, it has been
  possible to achieve a tremendous reduction (x100/x200) in the time needed to perform the same simulation.

## Multiphysics: Parametrised Stokes + Diffusion/Transport (chemical species)
The idea here is to couple the linear problem of the Stokes Equation, and then pass through the affine composition the compiled velocity field to a time-dependent problem of transport-diffusion of a scalar quantity like the concentration of species or temperature for instance.

$$
\begin{equation}
    \begin{cases}
        -\Delta \mathbf{b} +\nabla p=0 &\quad in \thinspace \Omega \\
        \text{div} \mathbf{b}=0  &\quad in \thinspace \Omega \\
        \mathbf{b}=[c_1,0]^T  &\quad on \thinspace\partial \Gamma_1^{in}\\
        \mathbf{b}=[c_2,c_3]^T &\quad on \thinspace\partial \Gamma_2^{in}\\
        \mathbf{b}=0 &\quad on \thinspace\partial \Omega /\Gamma_1^{in}\cup\Gamma_2^{in}\\
    \end{cases} 
\end{equation}
$$

and

```
\begin{equation}
\begin{cases}
    \frac{\partial u}{\partial t} -\frac{1}{2}\Delta u + \mathbf{b}_{\boldsymbol{\mu}}\cdot \nabla u=0 &\qquad in \thinspace \Omega\times(0,T)\\
    \nabla u \cdot \hat{n}=0 &\qquad on \thinspace \Gamma_{1}^{\text{out}}\cup\Gamma_{2}^{\text{out}}\\
    u=0 &\qquad on \thinspace \Gamma^{\text{walls}}\\
    u(\cdot,0)=\mathbf{1}_{\Gamma_{in}} &\qquad on \thinspace \Gamma^{\text{in}}
    \label{eq: Transport-diffusion_assign1}
\end{cases}
\end{equation}
```

Since the problem is affine, the affine-decomposition can be introduced on the parametrized term
```
A_{\boldsymbol{\mu}}=c_1\underbrace{\mathbf{b}_1\nabla u}_{A_1^1} + c_2\underbrace{\mathbf{b}_2\nabla u}_{A_2^2} +
                     c_3\underbrace{\mathbf{b}_3\nabla u}_{A_3^3}
```
