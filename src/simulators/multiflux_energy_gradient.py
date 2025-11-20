import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.cluster import KMeans
import os
from matplotlib.colors import Normalize

# === CONFIGURAÇÃO ===
NUM_PARTICLES = 4000
GRID_SIZE = 100
FLOW_SPEED = 4.0
VISCOSITY = 0.03
WALL_Y = 15
NUM_FRAMES = 180
OUTPUT_DIR = "media/videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)
GIF_PATH = os.path.join(OUTPUT_DIR, "multiflux_energy_gradient.gif")

# === INICIALIZAÇÃO ===
np.random.seed(42)
pos = np.random.rand(NUM_PARTICLES, 2) * [GRID_SIZE, GRID_SIZE - WALL_Y] + [0, WALL_Y]
vel = np.zeros((NUM_PARTICLES, 2))
vel[:, 0] = FLOW_SPEED

# Perturbação (disco voador)
pert_center = np.array([35, 65])
pert_radius = 7

fig, ax = plt.subplots(figsize=(10, 6))

def update(frame):
    global pos, vel
    ax.clear()

    # --- 1. Viscosidade (SPM simplificado) ---
    for i in range(NUM_PARTICLES):
        dists = np.linalg.norm(pos - pos[i], axis=1)
        neighbors = (dists < 6) & (dists > 0)
        if np.any(neighbors):
            dv = vel[neighbors] - vel[i]
            vel[i] += VISCOSITY * np.mean(dv, axis=0) * 0.5

    # --- 2. Perturbação ---
    dist_to_pert = np.linalg.norm(pos - pert_center, axis=1)
    in_pert = dist_to_pert < pert_radius
    strength = (pert_radius - dist_to_pert[in_pert]) / pert_radius
    vel[in_pert, 1] += strength * 1.2

    # --- 3. Atualiza posição ---
    pos += vel

    # --- 4. Parede (Arrasto Granular) ---
    hit_wall = pos[:, 1] < WALL_Y
    vel[hit_wall, 1] = -vel[hit_wall, 1] * 0.6
    pos[hit_wall, 1] = WALL_Y + np.abs(pos[hit_wall, 1] - WALL_Y)

    # --- 5. Re-injeção ---
    left = pos[:, 0] > GRID_SIZE
    pos[left, 0] = 0
    vel[left] = [FLOW_SPEED, 0]

    # --- 6. KMeans por direção + magnitude ---
    speed = np.linalg.norm(vel, axis=1) + 1e-8
    direction = vel / speed[:, None]
    features = np.hstack([direction, np.log(speed)[:, None]])
    kmeans = KMeans(n_clusters=4, n_init=10, random_state=frame).fit(features)
    labels = kmeans.labels_

    # --- 7. ENERGIA CINÉTICA POR SUBFLUXO ---
    energies = []
    for k in range(4):
        mask = labels == k
        if np.any(mask):
            E_k = 0.5 * np.mean(speed[mask]**2)
            energies.append(E_k)
        else:
            energies.append(0)
    energies = np.array(energies)

    # --- 8. NORMALIZAÇÃO DO GRADIENTE ---
    norm = Normalize(vmin=energies.min(), vmax=energies.max())
    cmap = plt.cm.inferno

    # --- 9. CORES POR PARTÍCULA (baseado no subfluxo) ---
    particle_colors = cmap(norm(energies[labels]))

    # --- 10. PLOT ---
    scatter = ax.scatter(pos[:, 0], pos[:, 1], c=particle_colors, s=4, alpha=0.8)
    ax.plot([0, GRID_SIZE], [WALL_Y, WALL_Y], 'cyan', lw=2, label='Superfície (β)')
    circle = plt.Circle(pert_center, pert_radius, color='lime', fill=False, lw=2, alpha=0.7)
    ax.add_artist(circle)

    # Legenda de energia
    for k in range(4):
        if energies[k] > 0:
            ax.scatter([], [], c=[cmap(norm(energies[k]))], s=50, label=f'Subfluxo {k}: E={energies[k]:.2f}')

    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.set_facecolor('#0a0a0a')
    ax.set_title(f"Multifluxo v3.0 | Frame {frame} | Subfluxos por Energia Cinética", color='white')
    ax.legend(facecolor='black', labelcolor='white', loc='upper right')

    plt.tight_layout()

# === ANIMAÇÃO ===
print("Gerando simulação com gradiente de energia...")
ani = FuncAnimation(fig, update, frames=NUM_FRAMES, interval=60)
ani.save(GIF_PATH, writer='pillow', fps=20, dpi=130)
print(f"Simulação salva em: {GIF_PATH}")
