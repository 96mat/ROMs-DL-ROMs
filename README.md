# POD-Galerking RB method
This method has been applied to the following affine problems
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
+ Now the FEM solution of this model, which is basically an advection-diffusion equation, is repeated for different (random) parameters to build the $\mathcal{M}_h$ space linked to the
   so-called snapshot matrix, upon which the POD decomposition is performed.
+ We get the functions needed to build the reduced model of the S.E.,  since the entire problem is projected in another space endowed with some special properties, it has been
  possible to achieve a tremendous reduction (x100/x200) in the time needed to perform the same simulation.

## Multiphysics: Stokes + Diffusion/Transport (chemical species)
...  READ-ME in progress
