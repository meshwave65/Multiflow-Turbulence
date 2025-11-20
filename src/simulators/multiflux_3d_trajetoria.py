# multiflux_3d_final_v2_compat.py
# VERSÃO FINAL COM CORREÇÃO DE COMPATIBILIDADE PARA VERSÕES ANTIGAS DO PYVISTA

import numpy as np
import pyvista as pv
import os

# Tenta iniciar um framebuffer virtual para máxima compatibilidade em servidores.
try:
    pv.start_xvfb()
except Exception:
    print("AVISO: xvfb não pôde ser iniciado. A simulação continuará.")

# === CONFIGURAÇÃO ===
NUM_PARTICLES = 4000
DOMAIN = [120, 70, 70]
FLOW_SPEED = 6.0
VISCOSITY = 0.01
WALL_Z = 8
DISCO_RADIUS = 15
DISCO_THICKNESS = 1.0
NUM_FRAMES = 400
OUTPUT_DIR = "media/3d_final_v2"
os.makedirs(OUTPUT_DIR, exist_ok=True)
VIDEO_PATH = os.path.join(OUTPUT_DIR, "multifluxo_dinamico_compat.mp4")

COLOR_LAMINAR = np.array([138, 43, 226])
COLOR_TURBULENT = np.array([255, 215, 0])
PERTURBATION_THRESHOLD = 0.5

# === INICIALIZAÇÃO ===
np.random.seed(42)
pos = np.random.rand(NUM_PARTICLES, 3) * DOMAIN
vel = np.zeros((NUM_PARTICLES, 3))
vel[:, 0] = FLOW_SPEED

disco_center = np.array([40, 35, 35])

injectors = [
    {'center': np.array([70, 25, 45]), 'radius': 8, 'strength': 1.5},
    {'center': np.array([90, 50, 25]), 'radius': 6, 'strength': 1.2},
]

# === FUNÇÃO SDF ===
def disco_sdf(point):
    p = point - disco_center
    d_xy = np.sqrt(p[0]**2 + p[1]**2)
    dist = max(d_xy - DISCO_RADIUS, abs(p[2]) - DISCO_THICKNESS / 2)
    return dist

# === CONFIGURAÇÃO INICIAL DO PLOTTER ===
plotter = pv.Plotter(off_screen=True, window_size=[1200, 800])
plotter.set_background('black')

grid = pv.ImageData(dimensions=(40, 25, 25), spacing=(3, 3, 3), origin=(0, 0, 0))
plotter.add_mesh(grid, style='wireframe', opacity=0.05, color='white')

disco_mesh = pv.Cylinder(center=disco_center, direction=[0, 0, 1], radius=DISCO_RADIUS, height=DISCO_THICKNESS, resolution=100)
plotter.add_mesh(disco_mesh, color='silver', metallic=True, roughness=0.1, opacity=0.7)

# Prepara o objeto PolyData para as partículas
points = pv.PolyData(pos)
particle_colors = np.tile(COLOR_LAMINAR, (NUM_PARTICLES, 1))
points['colors'] = particle_colors

# Adiciona as partículas à cena
# O nome 'particles' é importante para podermos atualizar o ator depois
plotter.add_mesh(points, name='particles', scalars='colors', rgb=True, point_size=5, render_points_as_spheres=True)

plotter.camera_position = [(150, 80, 90), (60, 35, 35), (0, 0, 1)]
plotter.camera.zoom(1.2)

# === FUNÇÃO DE ATUALIZAÇÃO DO FRAME ===
def update_scene(frame):
    global pos, vel, particle_colors

    # ... (Toda a lógica de física permanece a mesma) ...
    for i in range(NUM_PARTICLES):
        dists = np.linalg.norm(pos - pos[i], axis=1)
        neighbors = (dists < 8) & (dists > 0)
        if np.any(neighbors):
            dv = vel[neighbors] - vel[i]
            vel[i] += VISCOSITY * np.mean(dv, axis=0)

    sdf_vals = np.array([disco_sdf(p) for p in pos])
    near_disco = sdf_vals < 1.5
    if np.any(near_disco):
        for idx in np.where(near_disco)[0]:
            p = pos[idx]
            grad = np.zeros(3)
            eps = 0.01
            grad[0] = (disco_sdf(p + [eps, 0, 0]) - disco_sdf(p - [eps, 0, 0])) / (2 * eps)
            grad[1] = (disco_sdf(p + [0, eps, 0]) - disco_sdf(p - [0, eps, 0])) / (2 * eps)
            grad[2] = (disco_sdf(p + [0, 0, eps]) - disco_sdf(p - [0, 0, eps])) / (2 * eps)
            normal = grad / (np.linalg.norm(grad) + 1e-8)
            vel[idx] = vel[idx] - 1.5 * np.dot(vel[idx], normal) * normal

    for injector in injectors:
        dists_to_injector = np.linalg.norm(pos - injector['center'], axis=1)
        in_injector = dists_to_injector < injector['radius']
        if np.any(in_injector):
            push_direction = np.random.randn(np.sum(in_injector), 3)
            push_direction /= np.linalg.norm(push_direction, axis=1)[:, np.newaxis]
            vel[in_injector] += push_direction * injector['strength']

    pos += vel

    hit = pos[:, 2] < WALL_Z
    if np.any(hit):
        vel[hit, 2] = -vel[hit, 2] * 0.65
        pos[hit, 2] = WALL_Z + (WALL_Z - pos[hit, 2])

    out_of_bounds = pos[:, 0] > DOMAIN[0]
    if np.any(out_of_bounds):
        pos[out_of_bounds, 0] = 0
        vel[out_of_bounds] = [FLOW_SPEED, 0, 0]

    # Atualiza as cores
    perturbation = np.linalg.norm(vel[:, 1:], axis=1)
    for i in range(NUM_PARTICLES):
        if perturbation[i] > PERTURBATION_THRESHOLD:
            particle_colors[i] = COLOR_TURBULENT
        else:
            particle_colors[i] = COLOR_LAMINAR
    
    # ### CORREÇÃO FINAL: Atualiza os dados diretamente no objeto PolyData ###
    # Em vez de chamar um método do plotter, modificamos o objeto 'points' que já está na cena.
    # O plotter irá detectar a mudança no próximo render.
    points.points = pos
    points['colors'] = particle_colors
    
    # Adiciona o texto do frame
    plotter.add_text(f"Multifluxo Dinâmico (v4) | Frame {frame}", name="frame_text", position='upper_left', color='white', font_size=12)

# === GERAÇÃO DO VÍDEO ===
print("Iniciando simulação final (v4 compat)...")
plotter.open_movie(VIDEO_PATH, framerate=30)

# Renderiza o primeiro frame
print("Renderizando frame 0...")
plotter.render()
plotter.write_frame()

# Loop para os frames restantes
for frame in range(1, NUM_FRAMES):
    update_scene(frame)
    plotter.write_frame() # Escreve o frame atualizado para o vídeo
    if frame % 50 == 0:
        print(f"Renderizando frame {frame}/{NUM_FRAMES}")

plotter.close()
print(f"\nSUCESSO: Vídeo salvo em: {VIDEO_PATH}")

