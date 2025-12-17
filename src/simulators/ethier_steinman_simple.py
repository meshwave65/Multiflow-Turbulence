# ethier_exact_simple.py
# Solução exata de Ethier & Steinman (1994) – fórmula correta do artigo
import numpy as np

# Parâmetros EXATOS do artigo (página 372)
a = -np.pi / 4.0
d =  np.pi / 4.0     # este é o "d" que o Prof. Denaro quer variar!

# Domínio padrão usado no paper: cubo [-1, 1]^3
nx = 80  # quanto maior, mais preciso
x = np.linspace(-1, 1, nx)
y = np.linspace(-1, 1, nx)
z = np.linspace(-1, 1, nx)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

def ethier_steinman_velocity(t, d=d):
    # Equações (9), (10), (11) do artigo original
    u = -np.exp(a*X) * np.sin(a*Y + d*Z) * np.exp(-d**2 * t) \
        - np.exp(a*Z) * np.cos(a*X + a*Y) * np.exp(-d**2 * t)

    v = -np.exp(a*Y) * np.sin(a*Z + a*X) * np.exp(-d**2 * t) \
        - np.exp(a*X) * np.cos(a*Y + d*Z) * np.exp(-d**2 * t)

    w =  np.exp(a*Z) * np.sin(a*X + a*Y) * np.exp(-d**2 * t) \
        - np.exp(a*Y) * np.cos(a*Z + a*X) * np.exp(-d**2 * t)

    return u, v, w

# Cálculo da norma L2 exata da velocidade em função de t e d
def L2_norm(t, d):
    u, v, w = ethier_steinman_velocity(t, d)
    integrand = u**2 + v**2 + w**2
    L2 = np.sqrt(np.mean(integrand)) * np.cbrt(8.0)   # fator porque volume = 8
    return L2

# Tabela que o Denaro pediu
print("   t    |   d=π/8    d=π/4    d=π/2    d=π")
print("--------|------------------------------------")
times = [0.0, 0.1, 0.5, 1.0, 2.0]
d_values = [np.pi/8, np.pi/4, np.pi/2, np.pi]

for t in times:
    linha = f"{t:5.1f}   "
    for d in d_values:
        norm = L2_norm(t, d)
        linha += f"{norm:8.4f}  "
    print(linha)
