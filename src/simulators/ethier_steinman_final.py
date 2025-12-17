# ethier_final.py
from dolfinx import mesh
from dolfinx.mesh import create_box, CellType
from dolfinx.fem import Function, FunctionSpace, Expression, Constant
from mpi4py import MPI
import ufl
import numpy as np

a = -np.pi/4
d = np.pi/4

domain = create_box(MPI.COMM_WORLD,
                    [np.array([-1.,-1.,-1.0]), np.array([1.,1.,1.])],
                    [32,32,32], CellType.hexahedron)

V = FunctionSpace(domain, ("CG", 2))
u_ex = Function(V)

x = ufl.SpatialCoordinate(domain)
t = Constant(domain, 0.0)

u_exact = ufl.as_vector([
    (-ufl.exp(a*x[0]) * ufl.sin(a*x[1] + d*x[2]) 
     - ufl.exp(a*x[2]) * ufl.cos(a*x[0] + a*x[1])) * ufl.exp(-d**2 * t),

    (-ufl.exp(a*x[1]) * ufl.sin(a*x[2] + a*x[0]) 
     - ufl.exp(a*x[0]) * ufl.cos(a*x[1] + d*x[2])) * ufl.exp(-d**2 * t),

    ( ufl.exp(a*x[2]) * ufl.sin(a*x[0] + a*x[1]) 
     - ufl.exp(a*x[1]) * ufl.cos(a*x[2] + a*x[0])) * ufl.exp(-d**2 * t)
])

def L2(t_val):
    t.value = t_val
    expr = Expression(u_exact, V.element.interpolation_points())
    u_ex.interpolate(expr)
    norma = np.sqrt(domain.comm.allreduce(
        fem.assemble_scalar(fem.form(ufl.inner(u_ex, u_ex) * ufl.dx)), op=MPI.SUM))
    return norma

print("t =   ||u_ex||_L2")
print("----------------")
for tv in [0.0, 0.1, 0.5, 1.0, 2.0]:
    print(f"{tv:.1f}   {L2(tv):.6f}")
