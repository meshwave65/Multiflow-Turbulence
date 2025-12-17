import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# DATASET COMPLETO (precisa estar dentro do script!)
# ==========================================================

data = {
    32: [
        0.08803177, 0.03710556, 0.11507416, 0.11637878,
        0.14870453, 0.11758041, 0.02717209, 0.01128387,
        0.08042145, 0.13235855, 0.07518387, 0.05070496
    ],

    64: [
        0.08803177, 0.03710556, 0.11507416, 0.11637878,
        0.14870453, 0.11758041, 0.02717209, 0.01128387,
        0.08042145, 0.13235855, 0.07518387, 0.05070496
    ],

    192: [
        0.06268084, 0.15173792, 0.09802698, 0.06664135,
        0.12444842, 0.01610424, 0.07690430, 0.08270038,
        0.14097765, 0.05279767, 0.10026946, 0.02671079
    ],

    256: [
        0.08946609, 0.06707764, 0.09463120, 0.05112076,
        0.13870239, 0.13077545, 0.16088104, 0.01521301,
        0.08141327, 0.02925491, 0.06488800, 0.07657623
    ],

    384: [
        0.09754096, 0.05803539, 0.13558282, 0.14233059,
        0.15543055, 0.15151638, 0.01965784, 0.02051007,
        0.06295889, 0.04971766, 0.06197781, 0.04474103
    ]
}

# ==========================================================
# GRÁFICOS
# ==========================================================

resolutions = sorted(data.keys())
N_eff = [len(data[r]) for r in resolutions]

# FIGURA 1 – N_eff x resolução
plt.figure(figsize=(6,4))
plt.plot(resolutions, N_eff, marker='o')
plt.title("Effective Subflux Count (N_eff) vs Resolution")
plt.xlabel("Grid Resolution (N³)")
plt.ylabel("N_eff")
plt.grid(True)
plt.tight_layout()
plt.savefig("fig_neff_vs_resolution.png", dpi=220)
plt.close()

# FIGURA 2 – Top-5 cluster volumes
plt.figure(figsize=(10,6))
for r in resolutions:
    vols = sorted(data[r], reverse=True)[:5]
    plt.plot(range(1,6), vols, marker='o', label=f"{r}³")
plt.title("Top-5 Cluster Volume Fractions vs Resolution")
plt.xlabel("Rank")
plt.ylabel("Volume Fraction")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("fig_top5_vs_resolution.png", dpi=220)
plt.close()

# FIGURA 3 – Distribuição completa dos clusters
plt.figure(figsize=(10,6))
for r in resolutions:
    plt.plot(range(12), data[r], marker='o', label=f"{r}³")
plt.title("Cluster Volume Distribution (12 Subfluxes)")
plt.xlabel("Cluster ID")
plt.ylabel("Volume Fraction")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("fig_cluster_distribution_all_scales.png", dpi=220)
plt.close()

# ==========================================================
# CSV Consolidado
# ==========================================================

rows = []
for r in resolutions:
    for cid, vf in enumerate(data[r]):
        rows.append([r, cid, vf])

df = pd.DataFrame(rows, columns=["resolution", "cluster_id", "volume_fraction"])
df.to_csv("cluster_volumes_comparison.csv", index=False)

print("All figures and CSV successfully generated.")

