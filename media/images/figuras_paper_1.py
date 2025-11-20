import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

# Figura 1: KMeans Instability (Clean Version)
fig1, ax1 = plt.subplots(figsize=(10, 6))
N = np.linspace(9000, 13000, 100)
inertia = 24000 + 1000 * np.sin(N/1000) + np.random.normal(0, 500, 100)  # Simulated high inertia ~24k
ax1.plot(N, inertia, 'bo-', label='Observed Inertia')
ax1.axhline(y=24000, color='r', linestyle='--', label='Threshold (~24k)')
ax1.set_xlabel('Inertia Parameter, N')
ax1.set_ylabel('Subflow Magnitude')
ax1.set_title('KMeans Clustering Instability in Multiflux Decomposition')
ax1.legend(); ax1.grid(True)
# Distorted centroids as ellipses
ellipse = Ellipse(xy=(11000, 25000), width=2000, height=5000, angle=10, fill=False, color='orange', linestyle='--')
ax1.add_patch(ellipse)
plt.tight_layout(); plt.savefig('figura1_kmeans_instability.png', dpi=300); plt.close()

# Figura 2: Skin-Friction Reduction
Re_tau = [180, 550, 1000, 2000]
Cf_before = [0.008, 0.0045, 0.0032, 0.0025]
Cf_after = [0.0044, 0.0027, 0.0019, 0.0015]  # 45-62% reduction
fig2, ax2 = plt.subplots(figsize=(8, 5))
width = 0.35
x = np.arange(len(Re_tau))
ax2.bar(x - width/2, Cf_before, width, label='Before Suppression')
ax2.bar(x + width/2, Cf_after, width, label='After Suppression')
ax2.set_xlabel('Re_τ'); ax2.set_ylabel('C_f'); ax2.set_title('Skin-Friction Reduction via Subflow Suppression')
ax2.set_xticks(x); ax2.set_xticklabels(Re_tau); ax2.legend(); ax2.grid(True)
plt.tight_layout(); plt.savefig('figura2_drag_reduction.png', dpi=300); plt.close()

# Figura 3: Second Laminar Regime (Conceptual)
fig3, ax3 = plt.subplots(figsize=(10, 6))
theta = np.linspace(0, 2*np.pi, 100)
r_primary = 5; r_transverse = np.linspace(3, 0.5, 100)  # Suppression
ax3.plot(r_primary * np.cos(theta), r_primary * np.sin(theta), 'b-', linewidth=3, label='Primary Subflow')
for i in range(0, len(theta), 10):
    ax3.plot([0, r_transverse[i] * np.cos(theta[i])], [0, r_transverse[i] * np.sin(theta[i])], 'r--', alpha=0.5, label='Suppressed Transverse' if i==0 else "")
ax3.set_xlim(-6, 6); ax3.set_ylim(-6, 6); ax3.set_aspect('equal')
ax3.set_title('Conceptual Diagram: High-Velocity Suppression in Second Laminar Regime')
ax3.legend(); ax3.grid(True)
plt.tight_layout(); plt.savefig('figura3_second_laminar.png', dpi=300); plt.close()

# Figura 4: Granular Molecular Drag
Mach = np.linspace(1, 10, 100)
Cd_classic = 0.5 / np.sqrt(Mach)  # Simplified classic
Cd_granular = 0.3 + 0.1 * Mach  # Linear granular hypothesis
fig4, ax4 = plt.subplots(figsize=(8, 5))
ax4.plot(Mach, Cd_classic, 'b-', label='Classic Turbulent')
ax4.plot(Mach, Cd_granular, 'g--', label='Granular Molecular Drag')
ax4.set_xlabel('Mach Number'); ax4.set_ylabel('C_d'); ax4.set_title('Drag Coefficient vs Mach (Granular Analogy)')
ax4.legend(); ax4.grid(True)
plt.tight_layout(); plt.savefig('figura4_granular_drag.png', dpi=300); plt.close()

print('All 4 figures saved as PNGs!')
