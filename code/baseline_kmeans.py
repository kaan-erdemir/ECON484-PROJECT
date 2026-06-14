import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def run_kmeans_pipeline():
    print("--- Iteration 04: Baseline K-Means Execution Starting ---\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    input_path = os.path.join(project_root, 'cleaned_data', 'imf_dots_cleaned.csv')
    output_csv_path = os.path.join(project_root, 'cleaned_data', 'kmeans_cluster_assignments.csv')

    plots_dir = os.path.join(project_root, 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    output_plot_path = os.path.join(plots_dir, 'kmeans_pca_plot.png')

    try:
        print(f"Loading cleaned data from: {input_path}")
        df = pd.read_csv(input_path)

        df_pivot = df.pivot_table(
            index='Reporter',
            columns=['Partner', 'Year'],
            values='Export_Value_USD_Scaled',
            fill_value=0
        )
        print(f"\nFeature Matrix Shape: {df_pivot.shape}")

        print("\nApplying PCA (Principal Component Analysis)...")
        pca = PCA(n_components=2, random_state=42)
        pca_features = pca.fit_transform(df_pivot)

        print(f"Explained Variance (PC1): {pca.explained_variance_ratio_[0] * 100:.2f}%")
        print(f"Explained Variance (PC2): {pca.explained_variance_ratio_[1] * 100:.2f}%")

        print("\nApplying K-Means Clustering (k=3)...")
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        cluster_assignments = kmeans.fit_predict(pca_features)

        df_pivot['Cluster'] = cluster_assignments

        df_results = df_pivot[['Cluster']].reset_index()
        df_results.to_csv(output_csv_path, index=False)
        print(f"\n[SUCCESS] Cluster assignments saved to: {os.path.abspath(output_csv_path)}")

        print("\nGenerating and saving Scatter Plot...")
        plt.figure(figsize=(10, 6))
        sns.set_theme(style="whitegrid")

        scatter = sns.scatterplot(
            x=pca_features[:, 0],
            y=pca_features[:, 1],
            hue=cluster_assignments,
            palette='viridis',
            s=200,
            edgecolor='black'
        )

        plt.title('Baseline K-Means: Global Supply Chain Regimes (PCA Reduced)', fontsize=14)
        plt.xlabel('Principal Component 1', fontsize=12)
        plt.ylabel('Principal Component 2', fontsize=12)

        for i, country in enumerate(df_pivot.index):
            plt.text(pca_features[i, 0] + 0.05, pca_features[i, 1] + 0.05, country, fontsize=11, weight='bold')

        plt.legend(title='Regime Cluster')

        plt.savefig(output_plot_path)
        print(f"[SUCCESS] Plot saved to: {os.path.abspath(output_plot_path)}")
        plt.show()

    except FileNotFoundError:
        print(f"\n[ERROR] Cleaned data file not found at {input_path}.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_kmeans_pipeline()