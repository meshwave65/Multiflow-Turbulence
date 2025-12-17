# ethier_fenics.py
from dolfinx import mesh, fem, io
from dolfinx.fem import Function, FunctionSpace, Constant
from dolfinx.mesh import create_box, CellType
from mpi4py import MPI
import ufl
import numpy as np

# Parâmetros do benchmark
a = -np.pi / 4.0
d = np.pi / 4.0        # mude aqui para testar outros valores de d

# Malha cubo [-1,1]^3
n = 20
domain = create_box(MPI.COMM_WORLD,
                    [np.array([-1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0])],
                    [n, n, n], CellType.hexahedron)

V = fem.VectorFunctionSpace(domain, ("CG", 2))
Q = fem.FunctionSpace(domain, ("CG", 1))

u_ex = Function(V)
p_ex = Function(Q)

x = ufl.SpatialCoordinate(domain)
t = Constant(domain, 0.0)

# Solução exata EXATA do paper (equações 9–12)
u_exact = ufl.as_vector([
    -ufl.exp(a*x[0]) * ufl.sin(a*x[1] + d*x[2]) * ufl.exp(-d**2 * t)
    - ufl.exp(a*x[2]) * ufl.cos(a*x[0] + a*x[1]) * ufl.exp(-d**2 * t),

    -ufl.exp(a*x[1]) * ufl.sin(a*x[2] + a*x[0]) * ufl.exp(-d**2 * t)
    - ufl.exp(a*x[0]) * ufl.cos(a*x[1] + d*x[2]) * ufl.exp(-d**2 * t),

     ufl.exp(a*x[2]) * ufl.sin(a*x[0] + a*x[1]) * ufl.exp(-d**2 * t)
    - ufl.exp(a*x[1]) * ufl.cos(a*x[2] + a*x[0]) * ufl.exp(-d**2 * t)
])

p_exact = -0.5 * (
    ufl.exp(2*a*x[0]) + ufl.exp(2*a*x[2]) +
    2*ufl.sin(a*x[1] + d*x[2]) * ufl.cos(a*x[0] + a*x[1]) * ufl.exp(a*(x[0]+x[2]))
) * ufl.exp(-2*d**2 * t)

# Função para calcular norma L2 da velocidade exata
def compute_L2_velocity(t_value):
    t.value = t_value
    expr = fem.Expression(u_exact, V.element.interpolation_points())
    u_ex.interpolate(expr)
    L2 = np.sqrt(domain.comm.allreduce(
        fem.assemble_scalar(fem.form(ufl.inner(u_ex, u_ex) * ufl.dx)), op=MPI.SUM))
    return L2

# Teste
print("t      L2 norm da velocidade exata")
print("--------------------------------")
for t_val in [0.0, 0.1, 0.5, 1.0, 2.0]:
    norm = compute_L2_velocity(t_val)
    print(f"{t_val:4.1f}    {norm:12.6f}")
