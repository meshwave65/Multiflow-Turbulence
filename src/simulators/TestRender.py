# teste_render.py
# Objetivo: Testar a capacidade de renderização básica do PyVista no seu ambiente.

import pyvista as pv
import os

# Diretório de saída para a imagem de teste
OUTPUT_DIR = "media/teste_render"
os.makedirs(OUTPUT_DIR, exist_ok=True)
IMAGE_PATH = os.path.join(OUTPUT_DIR, "teste_render.png")

print("Iniciando teste de renderização básica do PyVista...")

try:
    # Tenta iniciar um framebuffer virtual. Essencial para ambientes sem tela (servidores, Docker).
    # Se falhar, não é um erro fatal, mas um aviso.
    try:
        pv.start_xvfb()
        print("INFO: Framebuffer virtual (Xvfb) iniciado com sucesso.")
    except Exception as xvfb_error:
        print(f"AVISO: Não foi possível iniciar o framebuffer virtual (Xvfb): {xvfb_error}")
        print("A simulação continuará, mas pode falhar se não houver uma tela gráfica disponível.")

    # Cria um plotter. off_screen=True é crucial para salvar arquivos sem abrir uma janela.
    plotter = pv.Plotter(off_screen=True) 
    
    # Adiciona um objeto 3D simples à cena.
    esfera = pv.Sphere(radius=5, center=(0, 0, 0))
    plotter.add_mesh(esfera, color='crimson', show_edges=True)
    
    # Adiciona um texto para confirmação.
    plotter.add_text("Teste de Renderização PyVista OK", position='upper_left', font_size=12, color='white')
    
    # Configura a câmera para uma visão padrão.
    plotter.camera_position = 'iso'
    plotter.camera.zoom(1.5)
    
    # Tira uma "foto" (screenshot) da cena e salva em um arquivo.
    print(f"Salvando screenshot de teste em: {IMAGE_PATH}")
    plotter.screenshot(IMAGE_PATH)
    
    # Fecha o plotter para liberar recursos.
    plotter.close()
    
    # Verifica se o arquivo foi realmente criado.
    if os.path.exists(IMAGE_PATH):
        print("\n=====================================================================")
        print(f"SUCESSO: Imagem de teste foi gerada em: {IMAGE_PATH}")
        print("Por favor, verifique o arquivo para confirmar que ele contém uma esfera vermelha.")
        print("Se a imagem estiver correta, seu ambiente de renderização está funcionando.")
        print("=====================================================================")
    else:
        print("\n=====================================================================")
        print("ERRO: O script foi executado, mas o arquivo de imagem não foi criado.")
        print("Isso pode indicar um problema silencioso no backend de renderização.")
        print("=====================================================================")


except Exception as e:
    print("\n=====================================================================")
    print(f"ERRO CRÍTICO: A renderização básica falhou com uma exceção.")
    print(f"Detalhes do erro: {e}")
    print("\nCausa Provável: Problema com a instalação do PyVista/VTK ou com os drivers gráficos (OpenGL).")
    print("Ação Recomendada: Verifique se você está em um ambiente com suporte gráfico ou se as dependências (libgl1-mesa-glx, xvfb) estão instaladas.")
    print("=====================================================================")


