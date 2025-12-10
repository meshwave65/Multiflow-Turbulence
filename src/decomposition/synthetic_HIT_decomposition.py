# -*- coding: utf-8 -*-
"""
This work is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)88

Multiflux Theory — Prova de conceito numérica (versão aprimorada)
Melhorias incluídas:
 - Normalização por conchas k para aproximar espectro E(k) ~ k^{-5/3}
 - Projeção solenoidal correta
 - Cálculo de invariantes locais: |ω|, Q, λ2
 - Clusterização KMeans + análise de N_eff sobre vários cortes volumétricos
 - Múltiplos slices (x, y, z), histograma de volumes e CSV de volumes
 - Parâmetros ajustáveis e saída organizada
Dependências: numpy, scipy, scikit-learn, matplotlib
"""

import numpy as np
from scipy.fft import fftn, ifftn, fftfreq
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import json
import datetime

# -----------------------
# Configuração (edite conforme necessário)
# -----------------------
N = 64                 # grid N^3
L = 2 * np.pi          # domínio [0, L]^3
SEED = 42
K_CLUSTERS = 12
VOLUME_CUTOFFS = [0.001, 0.002, 0.005, 0.01, 0.02]  # frações do domínio para testar N_eff
SAVE_DIR = "output_multiflux"
SAVE_FIG = True
SAVE_CSV = True
VERBOSE = True

# Cria diretório de saída com timestamp
os.makedirs(SAVE_DIR, exist_ok=True)
meta = {
    "N": N,
    "L": L,
    "seed": SEED,
    "k_clusters": K_CLUSTERS,
    "volume_cutoffs": VOLUME_CUTOFFS,
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
}
with open(os.path.join(SAVE_DIR, "meta.json"), "w") as f:
    json.dump(meta, f, indent=2)

np.random.seed(SEED)

# -----------------------
# 1) Construir rede de wavenumbers
# -----------------------
if VERBOSE: print(f"Building k-grid for N={N}, L={L} ...")
kx = 2 * np.pi * fftfreq(N, d=L/N)
ky = 2 * np.pi * fftfreq(N, d=L/N)
kz = 2 * np.pi * fftfreq(N, d=L/N)
KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
K2 = KX**2 + KY**2 + KZ**2
# small offset to avoid division by zero
K2 += 1e-30
K = np.sqrt(K2)

# compute magnitude flattened for shell binning
k_flat = K.ravel()
k_nonzero = k_flat[k_flat > 0]
kmin = k_nonzero.min()
kmax = k_nonzero.max()

# choose number of shells (roughly N/2)
n_shells = int(np.ceil(np.sqrt(3) * (N//2)))
# define shell edges linearly in k
shell_edges = np.linspace(kmin, kmax, n_shells+1)
# compute shell index per mode
k_shell_idx = np.digitize(K, bins=shell_edges)  # values 0..n_shells

# -----------------------
# 2) gerar amplitudes complexas aleatórias e impor espectro alvo
# -----------------------
if VERBOSE: print("Generating raw Fourier amplitudes (random phases) ...")
# 3 component random complex field
amp = (np.random.randn(3, N, N, N) + 1j * np.random.randn(3, N, N, N))

# Desired spectral shape: E(k) ~ k^{-5/3}
# We'll enforce shellwise normalization so that the integrated power per shell scales like k^{-5/3}.
if VERBOSE: print("Applying preliminary shell scaling and per-shell normalization to match E(k) ~ k^-5/3 ...")

# compute current power per shell
power_shell = np.zeros(n_shells + 2, dtype=np.float64)  # accommodate indices
count_shell = np.zeros_like(power_shell, dtype=int)

amp_power = np.sum(np.abs(amp)**2, axis=0)  # shape (N,N,N)
for idx in range(1, n_shells+1):
    mask_shell = (k_shell_idx == idx)
    count = np.count_nonzero(mask_shell)
    if count == 0:
        continue
    count_shell[idx] = count
    power_shell[idx] = amp_power[mask_shell].sum()

# desired power per shell ~ k_center^{-5/3}
shell_centers = 0.5 * (shell_edges[:-1] + shell_edges[1:])
desired_power_shell = np.zeros_like(power_shell)
for idx in range(1, n_shells+1):
    kc = shell_centers[idx-1]
    if kc <= 0:
        desired_power_shell[idx] = 0.0
    else:
        desired_power_shell[idx] = kc**(-5/3)

# avoid zero division and normalize desired_power_shell to total current power
# only for shells that have counts
available = (count_shell > 0)
desired_power_shell[~available] = 0.0
total_desired = desired_power_shell.sum()
total_current = power_shell.sum()
if total_desired <= 0 or total_current <= 0:
    raise RuntimeError("Empty spectral power or invalid desired spectrum.")
# scale desired to match total current power
scale_factor = total_current / total_desired
desired_power_shell *= scale_factor

# Now adjust amplitudes per shell: multiply modes in shell by sqrt(desired_power / current_power)
amp_adjust = np.ones_like(amp[0])
for idx in range(1, n_shells+1):
    mask_shell = (k_shell_idx == idx)
    if not np.any(mask_shell):
        continue
    curr = power_shell[idx]
    want = desired_power_shell[idx]
    if curr <= 0:
        g = 0.0
    else:
        g = np.sqrt(want / curr)
    amp_adjust[mask_shell] = g

# apply adjustment to all 3 components
amp *= amp_adjust

# -----------------------
# 3) projeção solenoidal (remover componente compressível)
# -----------------------
if VERBOSE: print("Applying solenoidal projection in Fourier space ...")
# compute k · amp
k_dot_amp = KX * amp[0] + KY * amp[1] + KZ * amp[2]   # shape (N,N,N)
# projection: amp_i -> amp_i - k_i * (k · amp) / |k|^2
amp[0] = amp[0] - KX * (k_dot_amp / K2)
amp[1] = amp[1] - KY * (k_dot_amp / K2)
amp[2] = amp[2] - KZ * (k_dot_amp / K2)

# ensure Hermitian symmetry so field is real in physical space
# For real fields, Fourier coefficients must satisfy: F(-k) = conj(F(k))
# We'll enforce symmetry by averaging with its conjugate at mirrored index.
if VERBOSE: print("Enforcing Hermitian symmetry (F(-k) = conj(F(k))) ...")
def enforce_hermitian(field_hat):
    # field_hat shape (N,N,N)
    fh = field_hat.copy()
    for i in range(N):
        for j in range(N):
            for k in range(N):
                ip = (-i) % N
                jp = (-j) % N
                kp = (-k) % N
                # average: set fh[ip,jp,kp] = conj(fh[i,j,k])
                fh[ip, jp, kp] = np.conj(fh[i, j, k])
    return fh

# apply per-component
amp[0] = enforce_hermitian(amp[0])
amp[1] = enforce_hermitian(amp[1])
amp[2] = enforce_hermitian(amp[2])

# -----------------------
# 4) converter para espaço físico (velocidade)
# -----------------------
if VERBOSE: print("IFFT to physical space ...")
u = np.real(ifftn(amp[0]))
v = np.real(ifftn(amp[1]))
w = np.real(ifftn(amp[2]))

KE_mean = 0.5 * np.mean(u*u + v*v + w*w)
if VERBOSE: print(f"Field generated — mean kinetic energy density: {KE_mean:.6e}")

# -----------------------
# 5) cálculo de gradientes via FFT
# -----------------------
if VERBOSE: print("Computing gradients via spectral differentiation ...")
def grad_fft(f):
    fhat = fftn(f)
    fx = np.real(ifftn(1j * KX * fhat))
    fy = np.real(ifftn(1j * KY * fhat))
    fz = np.real(ifftn(1j * KZ * fhat))
    return fx, fy, fz

du_dx, du_dy, du_dz = grad_fft(u)
dv_dx, dv_dy, dv_dz = grad_fft(v)
dw_dx, dw_dy, dw_dz = grad_fft(w)

# gradient tensor A_{ij} = ∂u_i/∂x_j  (shape 3x3xN x N x N)
A = np.array([[du_dx, du_dy, du_dz],
              [dv_dx, dv_dy, dv_dz],
              [dw_dx, dw_dy, dw_dz]])

# -----------------------
# 6) invariantes locais: vorticidade, Q, lambda2
# -----------------------
if VERBOSE: print("Computing invariants: vorticity magnitude, Q, lambda2 ...")
omega_x = dw_dy - dv_dz
omega_y = du_dz - dw_dx
omega_z = dv_dx - du_dy
vort_mag = np.sqrt(omega_x**2 + omega_y**2 + omega_z**2)

S = 0.5 * (A + np.transpose(A, (1,0,2,3,4)))
Omega = 0.5 * (A - np.transpose(A, (1,0,2,3,4)))

tr_Omega2 = np.sum(Omega**2, axis=(0,1))
tr_S2 = np.sum(S**2, axis=(0,1))
Q = 0.5 * (tr_Omega2 - tr_S2)

# compute M = S^2 + Omega^2 and its eigenvalues to get lambda2
S2 = np.einsum('il...,lj...->ij...', S, S)
Omega2 = np.einsum('il...,lj...->ij...', Omega, Omega)
M = S2 + Omega2
# reorder M to shape (N,N,N,3,3)
M = np.moveaxis(M, [0,1], [-2,-1])
eigvals = np.linalg.eigvalsh(M)   # shape (N,N,N,3)
# second largest eigenvalue
lambda2 = np.sort(eigvals, axis=-1)[..., -2]

# -----------------------
# 7) preparação dos dados para clusterização
# -----------------------
if VERBOSE: print("Preparing features and standardizing ...")
features = np.column_stack([vort_mag.ravel(), Q.ravel(), lambda2.ravel()])
# robust standardization (z-score)
means = features.mean(axis=0)
stds = features.std(axis=0) + 1e-12
X = (features - means) / stds

# -----------------------
# 8) KMeans clustering
# -----------------------
if VERBOSE: print(f"Running KMeans with k={K_CLUSTERS} ...")
kmeans = KMeans(n_clusters=K_CLUSTERS, n_init=20, max_iter=500, random_state=SEED)
labels_flat = kmeans.fit_predict(X)
labels = labels_flat.reshape((N, N, N))

unique, counts = np.unique(labels_flat, return_counts=True)
volumes = counts / labels_flat.size  # fraction of domain per cluster
# sort descending
order = np.argsort(counts)[::-1]
top5 = volumes[order][:5] * 100

# N_eff computation for default cutoff (0.5%)
default_cut = 0.005
N_eff_default = np.sum(counts > default_cut * labels_flat.size)

if VERBOSE:
    print("\n--- Results ---")
    print(f"N_eff (cutoff {default_cut*100:.2f}%): {N_eff_default}")
    print("Top5 cluster volumes (%): " + ", ".join(f"{v:.2f}" for v in top5))

# Evaluate N_eff across requested cutoff list
N_eff_vs_cut = {}
for c in VOLUME_CUTOFFS:
    N_eff_vs_cut[c] = int(np.sum(counts > c * labels_flat.size))

# -----------------------
# 9) Save volumes CSV and metadata
# -----------------------
if SAVE_CSV:
    csv_path = os.path.join(SAVE_DIR, "cluster_volumes.csv")
    header = "cluster_id,count,volume_fraction\n"
    with open(csv_path, "w") as f:
        f.write(header)
        for cid, cnt in zip(unique, counts):
            f.write(f"{int(cid)},{int(cnt)},{cnt/labels_flat.size:.8f}\n")
    if VERBOSE: print(f"Saved cluster volumes to {csv_path}")

meta.update({
    "KE_mean": float(KE_mean),
    "N_eff_default": int(N_eff_default),
    "N_eff_vs_cut": N_eff_vs_cut,
    "top5_volumes_pct": [float(x) for x in (top5.tolist())]
})
with open(os.path.join(SAVE_DIR, "meta.json"), "w") as f:
    json.dump(meta, f, indent=2)

# -----------------------
# 10) Visualizações: slices (xy, xz, yz), histogram de volumes
# -----------------------
if VERBOSE: print("Generating figures (slices and histograms) ...")
mid = N // 2
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# xy slice at mid z
im0 = axes[0,0].imshow(labels[:, :, mid], origin='lower', interpolation='nearest')
axes[0,0].set_title(f"Slice XY (z={mid})")
axes[0,0].set_xlabel("x"); axes[0,0].set_ylabel("y")
cbar0 = plt.colorbar(im0, ax=axes[0,0], fraction=0.046, pad=0.04)
cbar0.set_label("Subflux ID")

# xz slice at mid y
im1 = axes[0,1].imshow(labels[:, mid, :].T, origin='lower', interpolation='nearest')
axes[0,1].set_title(f"Slice XZ (y={mid})")
axes[0,1].set_xlabel("x"); axes[0,1].set_ylabel("z")
cbar1 = plt.colorbar(im1, ax=axes[0,1], fraction=0.046, pad=0.04)
cbar1.set_label("Subflux ID")

# yz slice at mid x
im2 = axes[1,0].imshow(labels[mid, :, :].T, origin='lower', interpolation='nearest')
axes[1,0].set_title(f"Slice YZ (x={mid})")
axes[1,0].set_xlabel("y"); axes[1,0].set_ylabel("z")
cbar2 = plt.colorbar(im2, ax=axes[1,0], fraction=0.046, pad=0.04)
cbar2.set_label("Subflux ID")

# histogram of cluster volumes
axes[1,1].bar(np.arange(len(counts)), volumes*100)
axes[1,1].set_title("Cluster volumes (%)")
axes[1,1].set_xlabel("cluster id (sorted by label index)")
axes[1,1].set_ylabel("volume (%)")
axes[1,1].set_ylim(0, max(volumes*100)*1.2)

plt.suptitle(f"Multiflux Theory — Instantaneous decomposition (N={N})\nN_eff={N_eff_default} (cutoff {default_cut*100:.2f}%)", fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

fig_path = os.path.join(SAVE_DIR, "multiflux_slices_and_hist.png")
if SAVE_FIG:
    plt.savefig(fig_path, dpi=200, bbox_inches='tight')
if VERBOSE: print(f"Saved figure to {fig_path}")

# also save individual slice images for convenience
plt.close()

# individual saves
plt.figure(figsize=(6,6))
plt.imshow(labels[:, :, mid], origin='lower', interpolation='nearest')
plt.title(f"Slice XY (z={mid})")
plt.xlabel("x"); plt.ylabel("y")
plt.colorbar(label="Subflux ID")
p = os.path.join(SAVE_DIR, "slice_xy.png"); plt.savefig(p, dpi=200, bbox_inches='tight'); plt.close()
plt.figure(figsize=(6,6))
plt.imshow(labels[:, mid, :].T, origin='lower', interpolation='nearest')
plt.title(f"Slice XZ (y={mid})")
plt.xlabel("x"); plt.ylabel("z")
plt.colorbar(label="Subflux ID")
p = os.path.join(SAVE_DIR, "slice_xz.png"); plt.savefig(p, dpi=200, bbox_inches='tight'); plt.close()
plt.figure(figsize=(6,6))
plt.imshow(labels[mid, :, :].T, origin='lower', interpolation='nearest')
plt.title(f"Slice YZ (x={mid})")
plt.xlabel("y"); plt.ylabel("z")
plt.colorbar(label="Subflux ID")
p = os.path.join(SAVE_DIR, "slice_yz.png"); plt.savefig(p, dpi=200, bbox_inches='tight'); plt.close()

# -----------------------
# 11) Salvar dados essenciais (numpy .npz) para reprodução
# -----------------------
npz_path = os.path.join(SAVE_DIR, "multiflux_data.npz")
np.savez_compressed(npz_path,
                    u=u, v=v, w=w,
                    vort_mag=vort_mag, Q=Q, lambda2=lambda2,
                    labels=labels, counts=counts, volumes=volumes,
                    meta=meta)
if VERBOSE: print(f"Saved dataset to {npz_path}")

# -----------------------
# 12) Relatório rápido em texto
# -----------------------
report = []
report.append("Multiflux HIT synthetic run report")
report.append(f"Grid: {N}^3; L={L}; seed={SEED}; k_clusters={K_CLUSTERS}")
report.append(f"Mean kinetic energy density: {KE_mean:.6e}")
report.append(f"N_eff (cutoff {default_cut*100:.2f}%): {N_eff_default}")
report.append("Top 5 cluster volumes (%): " + ", ".join(f"{v:.2f}" for v in top5))
report.append("N_eff vs cutoffs:")
for c, neff in N_eff_vs_cut.items():
    report.append(f"  cutoff {c*100:.2f}% -> N_eff = {neff}")
report_text = "\n".join(report)
txt_path = os.path.join(SAVE_DIR, "report.txt")
with open(txt_path, "w") as f:
    f.write(report_text)
if VERBOSE: print(f"Saved report to {txt_path}")

if VERBOSE:
    print("\nRun complete. Outputs in folder:", SAVE_DIR)
    print(report_text)

