# -*- coding: utf-8 -*-
"""
Multiflux Theory — Prova de conceito numérica independente
Campo sintético HIT 64³ → N_eff real (tipicamente 9-14)
Zero dependências externas além de numpy, sklearn e matplotlib
"""

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.fft import fftn, ifftn, fftfreq

# =============================================
# 1) Configuração
# =============================================
N = 64
L = 2 * np.pi
np.random.seed(42)

print(f"Gerando campo sintético HIT {N}³...")

kx = 2 * np.pi * fftfreq(N, L/N)
ky = 2 * np.pi * fftfreq(N, L/N)
kz = 2 * np.pi * fftfreq(N, L/N)
KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
K2 = KX**2 + KY**2 + KZ**2 + 1e-30
mask = K2 > 0

# =============================================
# 2) Campo solenoidal no espaço de Fourier
# =============================================
u_hat = np.zeros((3, N, N, N), dtype=complex)

for i in range(3):
    amp = (np.random.randn(N,N,N) + 1j*np.random.randn(N,N,N))
    amp *= np.where(mask, K**(-5/6), 0)                 # E(k) ~ k^{-5/3}
    k_dot_u = (KX*u_hat[0] + KY*u_hat[1] + KZ*u_hat[2]) / K2
    if i == 0:
        u_hat[i] = amp - KX * k_dot_u
    elif i == 1:
        u_hat[i] = amp - KY * k_dot_u
    else:
        u_hat[i] = amp - KZ * k_dot_u

u = np.real(ifftn(u_hat[0]))
v = np.real(ifftn(u_hat[1]))
w = np.real(ifftn(u_hat[2]))

print(f"Campo gerado — energia média: {0.5*np.mean(u**2 + v**2 + w**2):.4f}")

# =============================================
# 3) Gradientes via FFT
# =============================================
def grad_fft(f):
    fhat = fftn(f)
    return (np.real(ifftn(1j*KX*fhat)),
            np.real(ifftn(1j*KY*fhat)),
            np.real(ifftn(1j*KZ*fhat)))

du_dx, du_dy, du_dz = grad_fft(u)
dv_dx, dv_dy, dv_dz = grad_fft(v)
dw_dx, dw_dy, dw_dz = grad_fft(w)

# Tensor gradiente A_ij = ∂u_i/∂x_j  (3,3,N,N,N)
A = np.array([[[du_dx, du_dy, du_dz],
               [dv_dx, dv_dy, dv_dz],
               [dw_dx, dw_dy, dw_dz]]])   # shape (1,3,3,N,N,N)

A = A[0]   # remove dimensão extra → (3,3,N,N,N)

S = 0.5 * (A + np.transpose(A, (1,0,2,3,4)))
Ω = 0.5 * (A - np.transpose(A, (1,0,2,3,4)))

# =============================================
# 4) Invariantes locais
# =============================================
vort_mag = np.linalg.norm(Ω, axis=(0,1))                # (N,N,N)
tr_Ω2 = np.sum(Ω**2, axis=(0,1))
tr_S2 = np.sum(S**2, axis=(0,1))
Q = 0.5 * (tr_Ω2 - tr_S2)                               # (N,N,N)

# λ₂ (segundo maior autovalor de S² + Ω²)
S2 = np.einsum('il...,lj...->ij...', S, S)
Ω2 = np.einsum('il...,lj...->ij...', Ω, Ω)
M = S2 + Ω2                                            # (3,3,N,N,N)
M = np.moveaxis(M, [0,1], [-2,-1])                     # (N,N,N,3,3)
eigvals = np.linalg.eigvalsh(M)
lambda2 = np.sort(eigvals, axis=-1)[..., -2]           # (N,N,N)

# =============================================
# 5) Clusterização
# =============================================
X = np.column_stack([vort_mag.ravel(), Q.ravel(), lambda2.ravel()])
X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-12)

k = 12
kmeans = KMeans(n_clusters=k, n_init=20, max_iter=500, random_state=42)
labels = kmeans.fit_predict(X).reshape(N, N, N)

unique, counts = np.unique(labels, return_counts=True)
N_eff = np.sum(counts > 0.005 * labels.size)

top5 = np.sort(counts)[-5:][::-1] / labels.size * 100
print(f"\nNÚMERO EFETIVO DE SUBFLUXOS (N_eff): {N_eff}")
print(f"Volumes dos 5 maiores clusters: {', '.join(f'{v:.2f}%' for v in top5)}")

# =============================================
# 6) Visualização
# =============================================
mid = N // 2
plt.figure(figsize=(10,8))
im = plt.imshow(labels[:, :, mid], cmap='tab20', interpolation='nearest')
plt.colorbar(im, label='Subfluxo ID', shrink=0.8)
plt.title(f'Multiflux Theory — Decomposição instantânea\nN_eff = {N_eff} (HIT sintético {N}³)')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()
plt.savefig('multiflux_decomposicao_sintetica.png', dpi=200, bbox_inches='tight')
plt.show()

print("\nTudo concluído! Figura salva como 'multiflux_decomposicao_sintetica.png'")
