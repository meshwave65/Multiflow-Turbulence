# multiflux_3d_disco_v2.py
# Simulação 3D: Disco voador + Subfluxos + Energia + Arrasto Granular
# Requer: pip install pyvista numpy

import numpy as np
import pyvista as pv
import os

# === VERIFICAÇÃO DE DEPENDÊNCIAS ===
try:
    import pyvista as pv
except ImportError:
    raise ImportError("Instale: pip install pyvista")

# === CONFIGURAÇÃO ===
NUM_PARTICLES = 6000
DOMAIN = [120, 70, 70]
FLOW_SPEED = 6.0
VISCOSITY = 0.015
WALL_Z = 8
DISCO_RADIUS = 15
DISCO_THICKNESS = 1.0
NUM_FRAMES = 300
OUTPUT_DIR = "media/3d_v2"  # ### ALTERAÇÃO: Novo diretório de saída ###
os.makedirs(OUTPUT_DIR, exist_ok=True)
VIDEO_PATH = os.path.join(OUTPUT_DIR, "disco_voador_perturbacao.mp4")

# === INICIALIZAÇÃO ===
np.random.seed(42)
pos = np.random.rand(NUM_PARTICLES, 3) * DOMAIN
vel = np.zeros((NUM_PARTICLES, 3))
vel[:, 0] = FLOW_SPEED

# Disco voador (posição fixa)
disco_center = np.array([40, 35, 35])

# === FUNÇÃO SDF DO DISCO VOADOR ===
def disco_sdf(point):
    d = np.sqrt((point[0] - disco_center[0])**2 + (point[1] - disco_center[1])**2)
    h = abs(point[2] - disco_center[2])
    return max(abs(d - DISCO_RADIUS), h) - DISCO_THICKNESS / 2

# === PLOTTER 3D ===
plotter = pv.Plotter(off_screen=True, window_size=[1200, 800])
plotter.set_background('black')

# Grade de referência
grid = pv.ImageData()
grid.dimensions = np.array([40, 25, 25]) + 1
grid.spacing = (3, 3, 3)
grid.origin = (0, 0, 0)
plotter.add_mesh(grid, opacity=0.05, color='white')

# Disco voador (malha)
disco = pv.Disc(center=disco_center, inner=0, outer=DISCO_RADIUS, r_res=60, c_res=60)
disco = disco.extrude([0, 0, DISCO_THICKNESS], capping=True)
plotter.add_mesh(disco, color='silver', metallic=True, roughness=0.1)

# Partículas
points = pv.PolyData(pos)
# ### ALTERAÇÃO: Inicializa o novo escalar 'perturbation' ###
points['perturbation'] = np.zeros(NUM_PARTICLES)

# ### ALTERAÇÃO: Cria um mapa de cores customizado (Lilás -> Amarelo) ###
custom_cmap = pv.LookupTable(cmap='viridis')
custom_cmap.apply_cmap([
    (0.0, '#8A2BE2'),  # Lilás (BlueViolet) para baixa perturbação
    (0.5, '#4B0082'),  # Índigo para perturbação média
    (1.0, '#FFD700')   # Amarelo (Gold) para alta perturbação
])

# ### ALTERAÇÃO: Adiciona as partículas usando o novo escalar e mapa de cores ###
plotter.add_points(points, scalars='perturbation', cmap=custom_cmap, point_size=3, clim=[0, 2.5])

# Câmera
plotter.camera_position = [(180, 100, 120), (60, 35, 35), (0, 0, 1)]

# === ATUALIZAÇÃO POR FRAME ===
def update(frame):
    global pos, vel, points

    # 1. Viscosidade
    for i in range(NUM_PARTICLES):
        dists = np.linalg.norm(pos - pos[i], axis=1)
        neighbors = (dists < 8) & (dists > 0)
        if np.any(neighbors):
            dv = vel[neighbors] - vel[i]
            vel[i] += VISCOSITY * np.mean(dv, axis=0)

    # 2. Perturbação do disco
    sdf_vals = np.array([disco_sdf(p) for p in pos])
    near = sdf_vals < 6
    if np.any(near):
        strength = (6 - sdf_vals[near]) / 6
        vel[near, 2] += strength * 0.4
        vel[near, 1] += (np.random.rand(np.sum(near)) - 0.5) * 0.2

    # 3. Atualiza posição
    pos += vel

    # 4. Parede inferior (arrasto granular)
    hit = pos[:, 2] < WALL_Z
    if np.any(hit):
        vel[hit, 2] = -vel[hit, 2] * 0.65
        pos[hit, 2] = WALL_Z + (WALL_Z - pos[hit, 2])

    # 5. Re-injeção
    left = pos[:, 0] > DOMAIN[0]
    if np.any(left):
        pos[left, 0] = 0
        vel[left] = [FLOW_SPEED, 0, 0]

    # 6. Atualiza partículas
    points.points = pos
    # ### ALTERAÇÃO: Calcula a perturbação como a magnitude da velocidade transversal ###
    perturbation = np.linalg.norm(vel[:, 1:], axis=1)
    points['perturbation'] = perturbation

    # 7. Renderiza
    plotter.clear_actors()
    plotter.add_mesh(grid, opacity=0.05, color='white')
    plotter.add_mesh(disco, color='silver', metallic=True, roughness=0.1)
    # ### ALTERAÇÃO: Usa o novo escalar e mapa de cores na renderização ###
    plotter.add_points(points, scalars='perturbation', cmap=custom_cmap, point_size=3, clim=[0, 2.5])
    plotter.add_text(f"Multifluxo 3D | Perturbação | Frame {frame}", position='upper_left', color='white', font_size=12)
    plotter.write_frame()

# === GERA VÍDEO ===
print("Iniciando simulação 3D com visualização de perturbação...")
plotter.open_movie(VIDEO_PATH, framerate=30)

for frame in range(NUM_FRAMES):
    update(frame)
    if frame % 50 == 0:
        print(f"Frame {frame}/{NUM_FRAMES}")

plotter.close()
print(f"Vídeo salvo em: {VIDEO_PATH}")

