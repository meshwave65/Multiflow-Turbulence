import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# --- Parâmetros da Simulação ---
GRID_SIZE = 200
IMPACT_POS = (100, 100)
WAVE_SPEED = 2
NUM_FRAMES = 80
OUTPUT_DIR = "media/videos"  # Salvaremos o GIF na pasta de mídias

# --- Preparação do Ambiente ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
GIF_FILENAME = os.path.join(OUTPUT_DIR, "drop_analogy.gif")

x = np.arange(0, GRID_SIZE)
y = np.arange(0, GRID_SIZE)
X, Y = np.meshgrid(x, y)
distance_from_impact = np.sqrt((X - IMPACT_POS[1])**2 + (Y - IMPACT_POS[0])**2)

# --- Configuração da Figura ---
fig, ax = plt.subplots(figsize=(6, 6))

def update(frame):
    """Função que atualiza cada quadro da animação."""
    ax.clear()  # Limpa o eixo para o próximo quadro

    current_wave_radius = frame * WAVE_SPEED
    
    # Cria uma onda senoidal que se expande
    wave_amplitude = np.sin(distance_from_impact * 0.5 - current_wave_radius * 0.5)
    
    # Cria uma "máscara" para desenhar apenas um anel da onda, dando a impressão de propagação
    wave_mask = np.where(np.abs(distance_from_impact - current_wave_radius) < 8, 1, 0)
    
    water_surface = wave_amplitude * wave_mask

    # Desenha a superfície da água
    ax.imshow(water_surface, cmap='Blues', vmin=-1, vmax=1, animated=True)
    ax.set_title(f"Droplet Analogy: Emergent Order (Time: {frame})")
    ax.set_xticks([])
    ax.set_yticks([])
    
# --- Criação e Salvamento da Animação ---
print("Criando animação...")
ani = animation.FuncAnimation(fig, update, frames=NUM_FRAMES, interval=50)

try:
    print(f"Salvando GIF em '{GIF_FILENAME}'...")
    # Usamos o writer 'pillow' que é ótimo para GIFs
    ani.save(GIF_FILENAME, writer='pillow', fps=20, dpi=100)
    print("GIF salvo com sucesso!")
except Exception as e:
    print(f"\n--- AVISO: Não foi possível salvar o GIF. ---")
    print(f"Erro: {e}")
    print("Verifique se a biblioteca 'Pillow' está instalada: pip install Pillow")

# plt.show() # Comentado para não precisar de interação manual

print("Processo concluído.")

