import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score


def run_evaluation_pipeline():
    print("--- Iteration 05: Qualitative Assessment of K-Means Flaws Starting ---\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    input_path = os.path.join(project_root, 'cleaned_data', 'imf_dots_cleaned.csv')
    plots_dir = os.path.join(project_root, 'plots')
    output_plot_path = os.path.join(plots_dir, 'kmeans_silhouette_analysis.png')

    try:
        # 1. Veriyi Oku ve Pivot Et
        df = pd.read_csv(input_path)
        df_pivot = df.pivot_table(
            index='Reporter',
            columns=['Partner', 'Year'],
            values='Export_Value_USD_Scaled',
            fill_value=0
        )

        # 2. PCA ve K-Means İşlemlerini Tekrarla (Baseline ile tutarlılık için)
        pca = PCA(n_components=2, random_state=42)
        pca_features = pca.fit_transform(df_pivot)

        n_clusters = 3
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(pca_features)

        # 3. Silhouette Metriklerini Hesapla
        # Genel skor
        avg_silhouette = silhouette_score(pca_features, cluster_labels)
        # Her ülkenin bireysel skoru
        sample_silhouette_values = silhouette_samples(pca_features, cluster_labels)

        print(f"Overall Dataset Silhouette Score: {avg_silhouette:.4f}")
        print("\n--- Qualitative Country-by-Country Assessment ---")

        # Ülkelerin skorlarını rapora dök
        country_scores = []
        for i, country in enumerate(df_pivot.index):
            score = sample_silhouette_values[i]
            cluster = cluster_labels[i]
            country_scores.append({'Country': country, 'Cluster': cluster, 'Silhouette': score})
            print(f"Country: {country:<4} | Assigned Cluster: {cluster} | Silhouette Score: {score:>7.4f}")

        # 4. Silhouette Plot Grafiğini Çiz
        fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
        ax1.set_xlim([-0.2, 1])
        ax1.set_ylim([0, len(df_pivot) + (n_clusters + 1) * 10])

        y_lower = 10
        for i in range(n_clusters):
            # Her küme için skorları topla ve sırala
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i) / n_clusters)
            ax1.fill_betweenx(
                np.arange(y_lower, y_upper),
                0,
                ith_cluster_silhouette_values,
                facecolor=color,
                edgecolor=color,
                alpha=0.7,
                label=f'Cluster {i}'
            )

            # Küme etiketini grafiğe bas
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
            y_lower = y_upper + 10  # Bir sonraki küme için boşluk bırak

        ax1.set_title("K-Means Boundary & Geometric Flaw Analysis (Silhouette Plot)", fontsize=14)
        ax1.set_xlabel("Silhouette Coefficient Values", fontsize=12)
        ax1.set_ylabel("Cluster Label / Samples", fontsize=12)

        # Ortalama çizgisini çiz (Kırmızı kesikli çizgi)
        ax1.axvline(x=avg_silhouette, color="red", linestyle="--", label=f"Avg Score ({avg_silhouette:.2f})")
        ax1.set_yticks([])  # Ülke indekslerini temizle (Görsel temizlik için)
        ax1.legend(loc="upper right")

        # Grafiği Kaydet
        os.makedirs(plots_dir, exist_ok=True)
        plt.savefig(output_plot_path)
        print(f"\n[SUCCESS] Silhouette Plot saved to: {os.path.abspath(output_plot_path)}")
        plt.show()

    except FileNotFoundError:
        print(f"[ERROR] Cleaned data not found. Please run the pipeline sequentially.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_evaluation_pipeline()