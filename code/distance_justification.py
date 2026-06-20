import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, cophenet


def analyze_and_plot_distance_metrics():
    print("--- Iteration 06: Empirical Distance Metric Justification & Plotting ---\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'cleaned_data', 'imf_dots_cleaned.csv')
    plots_dir = os.path.join(project_root, 'plots')
    output_plot_path = os.path.join(plots_dir, 'distance_metric_fidelity.png')

    try:
        # 1. Temizlenmiş Veriyi Yükle ve Pivot Et
        df = pd.read_csv(input_path)
        df_pivot = df.pivot_table(
            index='Reporter',
            columns=['Partner', 'Year'],
            values='Export_Value_USD_Scaled',
            fill_value=0
        )

        X = df_pivot.values

        metrics = {
            'Euclidean': 'euclidean',
            'Manhattan (Cityblock)': 'cityblock',
            'Cosine': 'cosine'
        }

        # Grafik için verileri toplayacağımız listeler
        plot_labels = []
        plot_scores = []
        plot_colors = []

        print("=== Mathematical Fidelity via Cophenetic Correlation ===")
        print("-" * 80)

        linkages = ['average', 'complete', 'single']

        for name, metric_key in metrics.items():
            flat_dist = pdist(X, metric=metric_key)
            for link_method in linkages:
                try:
                    Z = linkage(flat_dist, method=link_method)
                    c, _ = cophenet(Z, flat_dist)

                    label = f"{name}\n({link_method.capitalize()})"
                    plot_labels.append(label)
                    plot_scores.append(c)

                    # En yüksek başarıya özel renk (Yeşil tonları), diğerlerine standart mavi
                    if metric_key == 'cityblock' and link_method == 'average':
                        plot_colors.append('#2ecc71')  # Parlak Yeşil (Zirve)
                    else:
                        plot_colors.append('#3498db')  # Standart Mavi

                    print(
                        f"Metric: {name:<22} | Linkage: {link_method.capitalize():<8} | Cophenetic Correlation (r): {c:.4f}")
                except Exception:
                    continue

            # Özel Durum: Ward Linkage sadece Euclidean ile çalışır
            if metric_key == 'euclidean':
                Z_ward = linkage(flat_dist, method='ward')
                c_ward, _ = cophenet(Z_ward, flat_dist)

                label = "Euclidean\n(Ward)"
                plot_labels.append(label)
                plot_scores.append(c_ward)
                plot_colors.append('#e74c3c')  # Kırmızı (En Kötü/K-Means Hatası)
                print(f"Metric: {name:<22} | Linkage: Ward     | Cophenetic Correlation (r): {c_ward:.4f}")

        print("-" * 80)

        # 2. GÖZ ALICI GRAFİK OLUŞTURMA AŞAMASI
        plt.figure(figsize=(12, 6))

        # Bar grafiğini çiz
        bars = plt.bar(plot_labels, plot_scores, color=plot_colors, edgecolor='black', alpha=0.85, width=0.6)

        # Barların üzerine net rakamsal değerleri yaz
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.01, f"{yval:.4f}", ha='center', va='bottom',
                     fontsize=9, fontweight='bold')

        plt.title(
            "Empirical Validation of Distance Metrics & Linkage Criteria\n(Cophenetic Correlation Coefficient Optimization - Higher is Better)",
            fontsize=13, fontweight='bold', pad=15)
        plt.ylabel("Cophenetic Correlation Coefficient (r)", fontsize=11, fontweight='bold')
        plt.xlabel("Mathematical Combinations (Distance Metric + Linkage)", fontsize=11, fontweight='bold')
        plt.ylim(0, 1.05)  # Skorlar 0 ile 1 arasında olduğu için tavanı sabitleyelim
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        # Önemli eşikleri belirtmek için yatay çizgiler ekleyelim
        plt.axhline(y=0.90, color='#2ecc71', linestyle=':', alpha=0.7, label='Excellent Fidelity (>0.90)')
        plt.axhline(y=0.70, color='#e67e22', linestyle=':', alpha=0.7, label='Acceptable Baseline (0.70)')

        # Grafiği Disk Üzerine Kaydet
        os.makedirs(plots_dir, exist_ok=True)
        plt.savefig(output_plot_path, bbox_inches='tight', dpi=300)
        print(
            f"\n[SUCCESS] Empirical benchmarking plot saved successfully to:\n -> {os.path.abspath(output_plot_path)}")
        plt.show()

    except FileNotFoundError:
        print("[ERROR] Cleaned data not found. Please ensure the pipeline preprocessing step ran successfully.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")


if __name__ == '__main__':
    analyze_and_plot_distance_metrics()