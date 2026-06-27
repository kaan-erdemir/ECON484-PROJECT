import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import matplotlib.pyplot as plt


def run_hierarchical_clustering():
    input_file = '../cleaned_data/imf_dots_cleaned.csv'
    output_cluster_file = '../cleaned_data/hierarchical_cluster_assignment.csv'
    output_plot = '../plots/dendrogram_complete_manhattan.jpg'

    # 1. Veriyi Yükleme
    print("Temizlenmiş makro ticaret verisi yükleniyor...")
    df_raw = pd.read_csv(input_file)

    # 2. PIVOT İŞLEMİ (Mimarinin Düzeltilmesi)
    # Satırlarda benzersiz Reporter (Ülkeler), sütunlarda Partner'lar olacak şekilde matrisi genişletiyoruz.
    # 'Value' kısmını kendi sütun adınıza göre (örn: 'Value', 'Trade_Volume' vb.) güncelleyin.
    trade_value_col = 'Value' if 'Value' in df_raw.columns else df_raw.select_dtypes(include=[np.number]).columns[0]

    print(f"Bilateral veriler pivot tabloya dönüştürülüyor (Metrik: {trade_value_col})...")
    df_pivot = df_raw.pivot_table(
        index='Reporter',
        columns='Partner',
        values=trade_value_col,
        aggfunc='sum'
    ).fillna(0)  # Ticaret olmayan rotalara 0 vererek matrisi koruyoruz

    # 3. Sayısal Matrisin Alınması
    X = df_pivot.values
    print(f"Matris Yapısı -> Ülke Sayısı: {X.shape[0]}, Özellik (Partner) Sayısı: {X.shape[1]}")

    # 4. Mesafe Matrisi ve Linkage Hesaplama
    print("Manhattan mesafe matrisi hesaplanıyor...")
    distance_matrix = pdist(X, metric='cityblock')

    print("Complete Linkage ile hiyerarşik ağaç oluşturuluyor...")
    Z = linkage(distance_matrix, method='complete')

    # 5. Dendrogram Çizimi ve Kaydedilmesi
    print("Dendrogram çiziliyor...")
    plt.figure(figsize=(15, 10))
    dendrogram(
        Z,
        labels=df_pivot.index,
        leaf_rotation=90,
        leaf_font_size=8,
        color_threshold=0.5 * max(Z[:, 2])
    )
    plt.title('Agglomerative Hierarchical Clustering (Manhattan + Complete)')
    plt.xlabel('Countries (Reporter)')
    plt.ylabel('Distance Threshold')
    plt.tight_layout()
    plt.savefig(output_plot, dpi=300)
    plt.close()
    print(f"Dendrogram kaydedildi: {output_plot}")

    # 6. Küme Atamaları (Zorunlu Sabit Küme)
    # Ülke bazlı yapıya geçtiğimiz için küme sayısını artık daha rasyonel (örn: 10 veya 15) tutabiliriz.
    num_clusters = 15
    print(f"Ülkeler {num_clusters} adet rejim kümesine bölünüyor...")
    cluster_labels = fcluster(Z, t=num_clusters, criterion='maxclust')

    # Sonuçları DataFrame'e Aktarma (Her ülke için sadece TEK satır olacak)
    results_df = pd.DataFrame({
        'Reporter': df_pivot.index,
        'Supply_Chain_Regime_ID': cluster_labels
    })

    results_df.to_csv(output_cluster_file, index=False)
    print(f"Kusursuz küme atamaları kaydedildi: {output_cluster_file}")


if __name__ == "__main__":
    run_hierarchical_clustering()