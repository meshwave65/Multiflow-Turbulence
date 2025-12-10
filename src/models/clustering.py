import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import MiniBatchKMeans
from sklearn.mixture import GaussianMixture
import hdbscan
from tqdm import tqdm

# Configurações
SNAPSHOT_FILE = "data/snapshot_Re550.npz"
OUTPUT_DIR = "data"
REPORT_FILE = "Relatorio_2_Clustering.md"
N_SAMPLES = 100000 # Número de pontos para amostragem

def load_data():
    """Carrega os dados do snapshot e prepara para o clustering."""
    try:
        data = np.load(SNAPSHOT_FILE)
        u = data['u']
        v = data['v']
        w = data['w']
        y = data['y']
        
        # O campo de velocidade tem shape (Ny, Nz, Nx)
        # O clustering será feito no espaço de velocidade (u, v, w)
        # O shape final para clustering deve ser (N_pontos, 3)
        
        # 1. Redimensionar para (N_pontos, 3)
        Ny, Nz, Nx = u.shape
        U_flat = u.flatten()
        V_flat = v.flatten()
        W_flat = w.flatten()
        Y_flat = np.repeat(y, Nz * Nx) # Coordenadas y repetidas
        
        # Criar o array de features (u, v, w)
        X = np.vstack([U_flat, V_flat, W_flat]).T
        
        # 2. Amostragem aleatória
        if X.shape[0] > N_SAMPLES:
            print(f"Amostrando {N_SAMPLES} de {X.shape[0]} pontos para clustering.")
            indices = np.random.choice(X.shape[0], N_SAMPLES, replace=False)
            X_sample = X[indices]
            Y_sample = Y_flat[indices]
        else:
            X_sample = X
            Y_sample = Y_flat
            indices = np.arange(X.shape[0])
            
        return X_sample, Y_sample, indices, Ny, Nz, Nx
    
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None, None, None, None, None, None

def run_clustering(X, method_name, params):
    """Executa o algoritmo de clustering."""
    print(f"\nExecutando {method_name}...")
    
    if method_name == "MiniBatchKMeans":
        model = MiniBatchKMeans(n_clusters=params['N'], random_state=0, n_init=3)
        labels = model.fit_predict(X)
        inertia = model.inertia_
        return labels, inertia
    
    elif method_name == "GaussianMixtureModel":
        model = GaussianMixture(n_components=params['N'], covariance_type='full', random_state=0, n_init=3)
        model.fit(X)
        labels = model.predict(X)
        # O GMM não tem inércia, usaremos o AIC/BIC ou log-likelihood
        score = model.score(X) * X.shape[0] # Log-likelihood total
        return labels, score
    
    elif method_name == "HDBSCAN":
        model = hdbscan.HDBSCAN(min_cluster_size=params['min_cluster_size'], core_dist_n_jobs=-1)
        labels = model.fit_predict(X)
        # HDBSCAN não tem inércia, usaremos o número de clusters
        n_clusters = len(np.unique(labels[labels != -1]))
        return labels, n_clusters
    
    return None, None

def analyze_results(X, Y, labels, method_name, metric):
    """Analisa e reporta os resultados do clustering."""
    
    unique_labels = np.unique(labels)
    n_clusters = len(unique_labels)
    
    # Excluir o cluster de ruído (-1) se for HDBSCAN
    if -1 in unique_labels:
        n_clusters -= 1
        noise_points = np.sum(labels == -1)
        total_points = len(labels)
        classified_fraction = (total_points - noise_points) / total_points
    else:
        classified_fraction = 1.0
        
    print(f"Método: {method_name}")
    print(f"Número de clusters (excluindo ruído): {n_clusters}")
    print(f"Fração de pontos classificados: {classified_fraction:.4f}")
    
    # Critério da teoria: encontrar entre 8 e 15 subfluxos coerentes que ocupem >90 % do volume.
    is_successful = (8 <= n_clusters <= 15) and (classified_fraction > 0.9)
    
    # Calcular centróides e volume de cada cluster
    cluster_info = []
    for label in unique_labels:
        if label == -1: continue
        
        cluster_points = X[labels == label]
        cluster_y = Y[labels == label]
        
        centroid = np.mean(cluster_points, axis=0)
        volume_fraction = len(cluster_points) / len(labels)
        
        cluster_info.append({
            'label': label,
            'centroid_u': centroid[0],
            'centroid_v': centroid[1],
            'centroid_w': centroid[2],
            'volume_fraction': volume_fraction,
            'mean_y': np.mean(cluster_y)
        })
        
    # Ordenar por volume
    cluster_info.sort(key=lambda x: x['volume_fraction'], reverse=True)
    
    # Gerar figura 3D (u, v, w) e 2D (y vs u)
    fig = plt.figure(figsize=(15, 6))
    
    # 3D Plot (u, v, w)
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_title(f'{method_name} - Espaço de Velocidade (u, v, w)')
    ax1.set_xlabel('u')
    ax1.set_ylabel('v')
    ax1.set_zlabel('w')
    
    # 2D Plot (y vs u)
    ax2 = fig.add_subplot(122)
    ax2.set_title(f'{method_name} - Perfil de Velocidade (y vs u)')
    ax2.set_xlabel('u')
    ax2.set_ylabel('y')
    
    # Plotar apenas os centróides para o 3D
    centroids = np.array([[c['centroid_u'], c['centroid_v'], c['centroid_w']] for c in cluster_info])
    ax1.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], c='red', marker='X', s=100, label='Centróides')
    
    # Plotar os pontos no 2D (y vs u)
    for i, info in enumerate(cluster_info):
        # Amostrar pontos para visualização (evitar sobrecarga)
        cluster_points = X[labels == info['label']]
        cluster_y = Y[labels == info['label']]
        
        # Plotar centróide no 2D
        ax2.scatter(info['centroid_u'], info['mean_y'], marker='o', s=50, label=f"Cluster {info['label']} ({info['volume_fraction']:.1%})")
        
    # Salvar figura
    fig_path = os.path.join(OUTPUT_DIR, f"clustering_{method_name}.png")
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close(fig)
    
    return {
        'method': method_name,
        'n_clusters': n_clusters,
        'classified_fraction': classified_fraction,
        'metric': metric,
        'is_successful': is_successful,
        'cluster_info': cluster_info,
        'fig_path': fig_path
    }

def generate_report(results):
    """Gera o Relatório 2 em Markdown."""
    
    report = "# Relatório 2: Identificação de Subfluxos (Clustering)\n\n"
    report += f"**Dados:** Snapshot instantâneo de DNS de canal ($Re_{{\\tau}}=550$)\n"
    report += f"**Amostragem:** {N_SAMPLES} pontos aleatórios do campo de velocidade $(u, v, w)$.\n\n"
    report += "**Critério de Sucesso da Teoria:** Encontrar entre 8 e 15 subfluxos coerentes que ocupem >90 % do volume.\n\n"
    
    for res in results:
        report += f"## 2.{res['method']}\n\n"
        report += f"**Parâmetros:** {res['metric']}\n"
        report += f"**Número de Clusters Encontrados:** {res['n_clusters']}\n"
        report += f"**Fração de Pontos Classificados:** {res['classified_fraction']:.2%}\n"
        report += f"**Resultado do Critério:** {'SUCESSO' if res['is_successful'] else 'FALHA'}\n\n"
        report += f"**Figura de Visualização:** {res['fig_path']}\n\n"
        
        report += "| Cluster | Fração de Volume | Centróide u | Centróide v | Centróide w | y Médio |\n"
        report += "| :---: | :---: | :---: | :---: | :---: | :---: |\n"
        
        for info in res['cluster_info'][:10]: # Top 10 clusters
            report += f"| {info['label']} | {info['volume_fraction']:.2%} | {info['centroid_u']:.4f} | {info['centroid_v']:.4f} | {info['centroid_w']:.4f} | {info['mean_y']:.4f} |\n"
        
        report += "\n"
        
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
        
    print(f"\nRelatório 2 gerado em: {REPORT_FILE}")

if __name__ == "__main__":
    X_sample, Y_sample, indices, Ny, Nz, Nx = load_data()
    
    if X_sample is None:
        exit()
        
    all_results = []
    
    # --- 1. MiniBatchKMeans ---
    for N in [8, 10, 12, 15]:
        labels, inertia = run_clustering(X_sample, "MiniBatchKMeans", {'N': N})
        metric_str = f"N={N}, Inércia={inertia:.2f}"
        all_results.append(analyze_results(X_sample, Y_sample, labels, f"MiniBatchKMeans (N={N})", metric_str))

    # --- 2. Gaussian Mixture Model ---
    for N in [8, 10, 12, 15]:
        labels, score = run_clustering(X_sample, "GaussianMixtureModel", {'N': N})
        metric_str = f"N={N}, Log-Likelihood={score:.2f}"
        all_results.append(analyze_results(X_sample, Y_sample, labels, f"GaussianMixtureModel (N={N})", metric_str))
        
    # --- 3. HDBSCAN ---
    for min_size in [50, 100, 200]:
        labels, n_clusters = run_clustering(X_sample, "HDBSCAN", {'min_cluster_size': min_size})
        metric_str = f"min_cluster_size={min_size}, Clusters={n_clusters}"
        all_results.append(analyze_results(X_sample, Y_sample, labels, f"HDBSCAN (min_size={min_size})", metric_str))

    generate_report(all_results)
    
    # Salvar o melhor resultado (usaremos o KMeans N=12 como padrão para as próximas etapas)
    # A teoria pede 8 a 15, vamos escolher um no meio.
    # O KMeans é o mais simples e direto para o conceito de "subfluxo médio".
    labels_kmeans_12, _ = run_clustering(X_sample, "MiniBatchKMeans", {'N': 12})
    
    # Salvar os labels do KMeans N=12 para uso futuro
    # É crucial mapear os labels da amostra de volta para o grid completo
    # Como usamos amostragem, precisamos rodar o KMeans no dataset completo para a próxima etapa.
    
    print("\nTreinando MiniBatchKMeans (N=12) no dataset completo para mapeamento...")
    
    # Recarregar o dataset completo
    data = np.load(SNAPSHOT_FILE)
    u = data['u']
    v = data['v']
    w = data['w']
    Ny, Nz, Nx = u.shape
    X_full = np.vstack([u.flatten(), v.flatten(), w.flatten()]).T
    
    # Treinar o modelo no dataset completo (ou usar o modelo treinado na amostra para prever o completo)
    # Usar o modelo treinado na amostra para prever o completo é mais rápido.
    model_kmeans_12 = MiniBatchKMeans(n_clusters=12, random_state=0, n_init=3)
    model_kmeans_12.fit(X_sample)
    
    # Prever labels para o dataset completo
    labels_full = model_kmeans_12.predict(X_full)
    
    # Salvar os labels completos e os centróides
    np.savez(os.path.join(OUTPUT_DIR, "clustering_results.npz"), 
             labels_full=labels_full, 
             centroids=model_kmeans_12.cluster_centers_,
             Ny=Ny, Nz=Nz, Nx=Nx)
    
    print("Labels e centróides do MiniBatchKMeans (N=12) salvos para o dataset completo.")
