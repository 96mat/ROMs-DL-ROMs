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
## Parametrized Shcrodinger's Equation 2D
<img width="697" height="277" alt="image" src="https://github.com/user-attachments/assets/d9ed2a52-2387-4a5d-b869-ac55f64f3c48" />



The affine decomposition of the problem is

$$  V_{\mu} =Ex_1+\Delta V \mathbf{1}_{(0,+\infty)}x_2 $$
+ Now the FEM solution of this model, which is a diffusion-reaction equation, is repeated for different (random) parameters to build the $\mathcal{M}\subset V_h$ subset linked to the
   so-called snapshot matrix, upon which the POD decomposition is performed.
+ We get the functions needed to build the reduced model of the S.E.,  since the entire problem is projected in another space endowed with some special properties, it has been
  possible to achieve a tremendous reduction **(x100/x200)** in the **time** needed to perform the same simulation.

https://github.com/user-attachments/assets/b75bf9f7-64e6-4f8b-a495-00f408ebc3c1



## Multiphysics: Parametrised Stokes + Diffusion/Transport (chemical species) 2D
The idea here is to couple the linear problem of the Stokes Equation, and then pass through the affine composition the compiled velocity field to a time-dependent problem of transport-diffusion of a scalar quantity like the concentration of species or temperature for instance.

<img width="689" height="342" alt="image" src="https://github.com/user-attachments/assets/41d48553-9d8d-44b7-8ada-0323b98c8f4b" />


and

<img width="834" height="210" alt="image" src="https://github.com/user-attachments/assets/e8f3ca40-0dd0-4fc3-bf1c-1208a119e14c" />


Since the problem is affine, the affine-decomposition can be introduced on the parametrized term
<img width="671" height="272" alt="image" src="https://github.com/user-attachments/assets/4915e8a8-404c-41ce-b8cf-3e04a0d889ad" />

The reconstructed velocity and concentration fields (reduced) employing an internal LU-factorization is **x600 times** faster than the original FOM with an error $\le 0.5$%


https://github.com/user-attachments/assets/6bf0d9e1-7fc2-41e2-b8bb-636d7704b85c


# Fisher-KPP Equation
<img width="634" height="163" alt="image" src="https://github.com/user-attachments/assets/cca0eba4-3c31-46a0-abc0-5e5b4a9ae0ee" />

where the parametrisation enters through

<img width="481" height="147" alt="image" src="https://github.com/user-attachments/assets/28f4ca39-1fb5-4bbb-9fa8-e1562eb11b87" />

here the surrogate model (approximately **10,000 times** faster than the FOM), varying the parameters outside the training set

![output1](https://github.com/user-attachments/assets/ff80472c-da72-48a9-bff8-c0179237c547)

and

![output3](https://github.com/user-attachments/assets/27baeed7-fc27-47ea-aca1-5758cb1a1643)

SINDy here was able to recover the values and the shape of the nonlinear reactive term, but not the full Laplacian operator that it "rediscovered" as a sort of relaxed transport term, solving the following minimisation problem

<img width="684" height="64" alt="image" src="https://github.com/user-attachments/assets/66fbb4c4-60c5-4e7d-9970-75384661ea49" />

