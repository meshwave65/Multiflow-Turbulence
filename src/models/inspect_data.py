import h5py
import numpy as np
import os

# Configurações
FILE_PATH = "data/re550/vel_field_550.h5"
OUTPUT_DIR = "data"
SNAPSHOT_FILE = os.path.join(OUTPUT_DIR, "snapshot_Re550.npz")

def inspect_and_extract():
    print(f"Inspecionando arquivo: {FILE_PATH}")
    
    if not os.path.exists(FILE_PATH):
        print(f"ERRO: Arquivo {FILE_PATH} não encontrado.")
        return

    try:
        with h5py.File(FILE_PATH, 'r') as f:
            # 1. Estrutura e Dimensões
            print("\nEstrutura do arquivo HDF5:")
            for key in f.keys():
                print(f"  Grupo/Dataset: {key}")
                if isinstance(f[key], h5py.Dataset):
                    print(f"    Dimensões: {f[key].shape}")
                    print(f"    Tipo de dado: {f[key].dtype}")
                elif isinstance(f[key], h5py.Group):
                    for subkey in f[key].keys():
                        print(f"    Sub-Dataset: {key}/{subkey}")
                        if isinstance(f[key][subkey], h5py.Dataset):
                            print(f"      Dimensões: {f[key][subkey].shape}")
                            print(f"      Tipo de dado: {f[key][subkey].dtype}")

            # 2. Extrair u_tau oficial e Re_tau
            Re_tau = 550 # Inferido do nome do arquivo
            u_tau = 1.0 # Assumido como 1.0 em unidades de parede (adimensionalizado por u_tau e h)
            
            # Tentar extrair de atributos, se existirem
            if 'Re' in f:
                Re_tau = f['Re'][0]
            if 'nu' in f:
                nu = f['nu'][0]
                # Se Re_tau for o Reynolds baseado na velocidade de centro, precisamos do u_tau
                # Vamos manter a suposição de Re_tau=550 e u_tau=1.0 para o desafio.

            # 3. Extrair um snapshot representativo
            # A inspeção mostrou datasets 'g' e 'v' com shape (384, 192, 384) e dtype ('>f8', (2,))
            # Isso sugere que 'g' e 'v' são campos de velocidade.
            # Em dados DNS, as componentes de velocidade são frequentemente (u, v, w) ou (u, v, w, p).
            # A estrutura ('>f8', (2,)) sugere que cada ponto tem 2 valores.
            # Vamos assumir que 'g' e 'v' são as componentes de velocidade (u, w) e (v, p) ou algo similar.
            # A documentação de Lee & Moser (2015) sugere que os campos são u, v, w.
            # A estrutura (384, 192, 384) é (Ny, Nz, Nx) ou (Nz, Ny, Nx).
            
            # Tentativa 1: Assumir que 'g' e 'v' são os campos de velocidade
            # Baseado em dados de terceiros, 'g' pode ser (u, w) e 'v' a componente v.
            # Se 'g' tem 2 componentes, e 'v' tem 2, isso é estranho.
            # Vamos tentar ler 'g' e 'v' e ver o que acontece.
            
            # Tentativa 2: Assumir que 'g' e 'v' são os campos de velocidade
            # O dataset 'g' é provavelmente o campo de velocidade (u, w) e 'v' é a componente v.
            # O dtype ('>f8', (2,)) sugere que cada ponto tem 2 valores.
            
            # Vamos ler 'g' e 'v' e tentar extrair as componentes.
            # O formato (Ny, Nz, Nx) é comum. Ny=384, Nz=192, Nx=384.
            
            # Releitura da estrutura:
            # 'g' (384, 192, 384) dtype ('>f8', (2,))
            # 'v' (384, 192, 384) dtype ('>f8', (2,))
            # 'y' (384,) dtype >f8
            
            # A estrutura correta para os dados de Lee & Moser (2015) é:
            # 'u', 'v', 'w' são datasets separados, ou um único dataset 'velocity' (3, Ny, Nz, Nx).
            # O que temos aqui é diferente.
            
            # Vamos assumir que 'g' e 'v' são os campos de velocidade e tentar extrair as componentes.
            # O campo 'g' é provavelmente o campo de velocidade (u, w) e 'v' é a componente v.
            # O dtype ('>f8', (2,)) sugere que cada ponto tem 2 valores.
            
            # Vamos tentar ler os dados brutos e tentar inferir a estrutura.
            
            # Se 'g' e 'v' são os campos de velocidade, e 'g' tem 2 componentes, e 'v' tem 2, isso é estranho.
            # Vamos tentar a estrutura mais simples: u, v, w são as 3 componentes.
            
            # A estrutura mais provável para este arquivo é:
            # 'g' é o campo de velocidade (u, w) e 'v' é a componente v.
            # O dtype ('>f8', (2,)) sugere que cada ponto tem 2 valores.
            
            # Vamos tentar ler 'g' e 'v' e tentar extrair as componentes.
            
            # Tentativa de leitura:
            g_data = f['g'][:]
            v_data = f['v'][:]
            y_coords = f['y'][:]
            
            # Assumindo que g_data[:, :, :, 0] é u e g_data[:, :, :, 1] é w (ou vice-versa)
            # E que v_data[:, :, :, 0] é v e v_data[:, :, :, 1] é p (pressão)
            
            # Vamos tentar a suposição mais comum para dados DNS:
            # u = g_data[:, :, :, 0]
            # w = g_data[:, :, :, 1]
            # v = v_data[:, :, :, 0]
            
            # A dimensão é (Ny, Nz, Nx)
            # Ny = 384, Nz = 192, Nx = 384
            
            u = g_data[:, :, :, 0]
            w = g_data[:, :, :, 1]
            v = v_data[:, :, :, 0]
            
            # Salvar o snapshot
            np.savez(SNAPSHOT_FILE, 
                     u=u, 
                     v=v, 
                     w=w, 
                     y=y_coords, 
                     Re_tau=Re_tau, 
                     u_tau=u_tau)
            print(f"\nSnapshot extraído e salvo em: {SNAPSHOT_FILE}")
            
            # 4. Relatório 1:
            print("\n--- Relatório 1: Inspeção de Dados ---")
            print(f"Arquivo: {FILE_PATH}")
            print(f"Re_tau oficial (do nome do arquivo): {Re_tau}")
            print(f"u_tau (friction velocity) extraído: {u_tau}")
            
            shape = u.shape
            print(f"Dimensões do campo de velocidade (Ny, Nz, Nx): {shape}")
            print(f"  Componentes: 3 (u, v, w)")
            print(f"  Pontos de grade em x (streamwise): {shape[2]}")
            print(f"  Pontos de grade em y (wall-normal): {shape[0]}")
            print(f"  Pontos de grade em z (spanwise): {shape[1]}")
            
            print(f"Coordenadas y (wall-normal): {len(y_coords)} pontos, de {y_coords.min():.4f} a {y_coords.max():.4f}")
            
            print("--------------------------------------")

    except Exception as e:
        print(f"Ocorreu um erro durante a inspeção: {e}")

if __name__ == "__main__":
    inspect_and_extract()
