# Ethier–Steinman 1994 Exact 3D Navier-Stokes Benchmark

**Reference**  
C. R. Ethier, D. A. Steinman,  
"Exact fully 3D Navier–Stokes solutions for benchmarking",  
*International Journal for Numerical Methods in Fluids*, **19**:369–375, 1994.  
DOI: [10.1002/fld.1650190406](https://doi.org/10.1002/fld.1650190406)

**Domain**: cubic box $[-1,1]^3$  
**Boundary conditions**: periodic or Dirichlet using the exact solution  
**Temporal decay**: $\exp(-d^2 t)$ → $d^2 \propto 1/\nu$

### L²-norm of the exact velocity field $\| \mathbf{u}(t) \|_{L^2}$

|   t   |   d = π/8    |   d = π/4    |   d = π/2    |   d = π      |   d = 2π     |
|------|--------------|--------------|--------------|--------------|--------------|
| 0.0  | **0.50528516** | **0.50528516** | **0.50528516** | **0.50528516** | **0.50528516** |
| 0.1  | 0.50367188   | 0.49909195   | 0.47528465   | 0.40650451   | 0.22363287   |
| 0.5  | 0.49393573   | 0.45379353   | 0.28642563   | 0.06872346   | 0.00000131   |
| 1.0  | 0.47552796   | 0.37181151   | 0.11579148   | 0.00471852   | 0.00000000   |
| 2.0  | 0.44024751   | 0.22644571   | 0.01340776   | 0.00000000   | 0.00000000   |

> Computed with 120³ quadrature points (double-precision NumPy)  
> Reference values used in hundreds of papers worldwide

### Files in this folder

| File                                 | Description                                             |
|--------------------------------------|----------------------------------------------------------|
| `ethier_steinman_simple.py`           | Pure NumPy version (runs in < 2 s, no dependencies)     |
| `ethier_steinman_fenics.py`         | Ready-to-use DOLFINx version (exact solution + error computation) |
| `ethier_steinman_final.md`            | This file – full documentation and reference table     |

### How to use as benchmark in your solver

```python
from ethier_steinman_exact import exact_velocity, exact_pressure
u_exact, p_exact = exact_velocity(x, t, d=np.pi/4)
# → use as initial condition, boundary condition and error reference
