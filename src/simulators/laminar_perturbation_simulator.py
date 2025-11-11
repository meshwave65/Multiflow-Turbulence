import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# --- Parâmetros da Simulação ---
NUM_PARTICLES = 5000       # Número de partículas de fluido (representando subfluxos)
GRID_SIZE = 100            # Tamanho do domínio da simulação
FLOW_SPEED = 1.5           # Velocidade base do fluxo laminar (horizontal)
PERTURBATION_STRENGTH = 1.0 # Força da perturbação (velocidade vertical adicionada)
INTERACTION_STRENGTH = 0.1 # Força com que as partículas se repelem (cria a "desordem")
NUM_FRAMES = 150           # Duração da animação

# --- Diretório de Saída ---
OUTPUT_DIR = "media/videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)
GIF_FILENAME = os.path.join(OUTPUT_DIR, "laminar_perturbation.gif")

# --- Inicialização das Partículas ---
# Posições iniciais aleatórias no grid
positions = np.random.rand(NUM_PARTICLES, 2) * GRID_SIZE
# Todas as partículas começam com velocidade laminar (horizontal)
velocities = np.zeros((NUM_PARTICLES, 2))
velocities[:, 0] = FLOW_SPEED

# --- Definição da Perturbação ---
# Uma área circular no meio do caminho
PERTURBATION_POS = np.array([GRID_SIZE / 3, GRID_SIZE / 2])
PERTURBATION_RADIUS = 8

# --- Configuração da Figura ---
fig, ax = plt.subplots(figsize=(10, 5))

# --- Função de Animação ---
def update(frame):
    global positions, velocities
    ax.clear()

    # 1. Movimento Básico: Adiciona a velocidade à posição
    positions += velocities

    # 2. Lógica da Perturbação
    # Encontra partículas dentro da zona de perturbação
    dist_from_pert = np.linalg.norm(positions - PERTURBATION_POS, axis=1)
    in_perturbation_zone = dist_from_pert < PERTURBATION_RADIUS
    
    # Aplica uma "força" vertical (desvio) a essas partículas
    # O desvio é maior no centro da perturbação
    deviation_force = (PERTURBATION_RADIUS - dist_from_pert[in_perturbation_zone]) / PERTURBATION_RADIUS
    velocities[in_perturbation_zone, 1] += (np.random.rand(np.sum(in_perturbation_zone)) - 0.5) * PERTURBATION_STRENGTH * deviation_force

    # 3. Lógica de Interação (Causa da "Turbulência")
    # Partículas com velocidade vertical significativa (subfluxos desviados) afetam suas vizinhas
    turbulent_particles = np.where(np.abs(velocities[:, 1]) > 0.1)[0]
    for idx in turbulent_particles:
        # Encontra vizinhos próximos
        distances = np.linalg.norm(positions - positions[idx], axis=1)
        neighbors = (distances < 3) & (distances > 0)
        # Transfere um pouco da velocidade vertical para os vizinhos
        velocities[neighbors, 1] += velocities[idx, 1] * INTERACTION_STRENGTH
        # Amortece a velocidade da partícula original para conservar energia (simplificado)
        velocities[idx, 1] *= 0.95 

    # 4. Lógica de Fronteira (Re-injeção de Partículas)
    # Partículas que saem pela direita, reaparecem na esquerda
    off_screen_right = positions[:, 0] > GRID_SIZE
    positions[off_screen_right, 0] = 0
    positions[off_screen_right, 1] = np.random.rand(np.sum(off_screen_right)) * GRID_SIZE
    # Reseta a velocidade dessas partículas para laminar puro
    velocities[off_screen_right, 1] = 0
    velocities[off_screen_right, 0] = FLOW_SPEED

    # 5. Visualização
    # Colore as partículas pela magnitude da sua velocidade "turbulenta" (vertical)
    colors = np.abs(velocities[:, 1])
    ax.scatter(positions[:, 0], positions[:, 1], s=2, c=colors, cmap='viridis', vmin=0, vmax=1.5)
    
    # Desenha a zona de perturbação para referência
    pert_circle = plt.Circle(PERTURBATION_POS, PERTURBATION_RADIUS, color='r', fill=False, linestyle='--', alpha=0.5)
    ax.add_artist(pert_circle)

    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.set_facecolor('black')
    ax.set_title(f"Laminar Flow Perturbation (Frame: {frame})")
    ax.set_xticks([])
    ax.set_yticks([])

# --- Criação e Salvamento da Animação ---
print("Criando simulação de perturbação de fluxo...")
ani = animation.FuncAnimation(fig, update, frames=NUM_FRAMES, interval=50)

try:
    print(f"Salvando GIF em '{GIF_FILENAME}'...")
    ani.save(GIF_FILENAME, writer='pillow', fps=20, dpi=120)
    print("GIF salvo com sucesso!")
except Exception as e:
    print(f"\n--- AVISO: Não foi possível salvar o GIF. ---")
    print(f"Erro: {e}")
    print("Verifique se as bibliotecas 'matplotlib' e 'Pillow' estão instaladas.")

print("Processo concluído.")

