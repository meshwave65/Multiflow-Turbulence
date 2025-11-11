import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Parâmetros da Simulação ---
GRID_SIZE = 200      # Tamanho do nosso "lago" (GRID_SIZE x GRID_SIZE)
IMPACT_POS = (100, 100) # Posição (y, x) onde a gota cai
WAVE_SPEED = 2       # Velocidade de propagação da onda
NUM_FRAMES = 80      # Duração da animação
FILENAME = "drop_analogy.png" # Nome do arquivo de saída

# --- Preparação do Ambiente ---

# Cria uma grade 2D para representar o lago.
# Usamos np.meshgrid para criar matrizes de coordenadas X e Y.
x = np.arange(0, GRID_SIZE)
y = np.arange(0, GRID_SIZE)
X, Y = np.meshgrid(x, y)

# Calcula a distância de cada ponto na grade até o ponto de impacto.
# Esta é a base para saber onde a onda está em cada momento.
distance_from_impact = np.sqrt((X - IMPACT_POS[1])**2 + (Y - IMPACT_POS[0])**2)

# --- Função de Animação ---
# Esta função é chamada para cada quadro (frame) da animação.
def update(frame):
    """
    Calcula e desenha o estado da onda para um determinado quadro de tempo.
    'frame' é o número do quadro atual, que usamos como nosso 'tempo'.
    """
    # Limpa o gráfico anterior para desenhar o novo.
    plt.cla()

    # Calcula a posição atual da frente de onda.
    current_wave_radius = frame * WAVE_SPEED

    # Cria a onda: usamos uma função seno que depende da distância e do tempo.
    # A onda só existe perto do raio atual, criando um efeito de propagação.
    # A condição 'np.abs(distance_from_impact - current_wave_radius) < 5' cria um anel.
    wave_amplitude = np.sin(distance_from_impact - current_wave_radius)
    wave_mask = np.where(np.abs(distance_from_impact - current_wave_radius) < 5, 1, 0)
    
    # A superfície da água é a combinação da amplitude e da máscara.
    water_surface = wave_amplitude * wave_mask

    # --- Visualização ---
    # Desenha a superfície da água usando um mapa de cores.
    # 'cmap' define o esquema de cores (ex: 'viridis', 'plasma', 'Blues').
    # 'vmin' e 'vmax' fixam a escala de cores para evitar cintilação.
    im = plt.imshow(water_surface, cmap='Blues', vmin=-1, vmax=1, animated=True)
    
    # Configurações do gráfico
    plt.title(f"Analogia da Gota: Ordem Emergente (Tempo: {frame})")
    plt.xlabel("Posição X")
    plt.ylabel("Posição Y")
    
    # Remove os eixos para um visual mais limpo
    plt.xticks([])
    plt.yticks([])
    
    return [im]

# --- Execução Principal ---

# Cria a figura e os eixos para a animação.
fig, ax = plt.subplots(figsize=(8, 8))

# Cria o objeto de animação.
# 'fig' é a figura onde a animação acontece.
# 'update' é a função que desenha cada quadro.
# 'frames' é o número total de quadros a serem gerados.
# 'interval' é o tempo em milissegundos entre os quadros.
# 'blit=True' otimiza a renderização.
ani = animation.FuncAnimation(fig, update, frames=NUM_FRAMES, interval=50, blit=True)

# 1. Exibe a animação na tela.
print("Exibindo a animação na tela...")
plt.show()

# 2. Salva o último quadro como uma imagem PNG.
# Recalculamos o último quadro para garantir que temos a imagem final.
print(f"Salvando o último quadro como '{FILENAME}'...")
fig_save, ax_save = plt.subplots(figsize=(8, 8))
plt.sca(ax_save) # Define o eixo atual para o de salvamento
update(NUM_FRAMES - 1) # Chama a função de atualização para o último quadro
plt.savefig(FILENAME, dpi=150, bbox_inches='tight')
plt.close(fig_save)

print("Processo concluído.")


