import pandas as pd


def parse_tax_havens():
    input_cluster_file = '../cleaned_data/hierarchical_cluster_assignment.csv'
    output_main_regimes = '../cleaned_data/main_supply_chain_regimes.csv'
    output_outliers = '../cleaned_data/isolated_tax_havens.csv'

    df_clusters = pd.read_csv(input_cluster_file)

    # KESİN ÇÖZÜM: Eşiği 0 yapıyoruz.
    # Böylece hiçbir ülke izole edilmeyecek, hepsi ana rejime geçecek.
    outlier_threshold = 0

    cluster_counts = df_clusters['Supply_Chain_Regime_ID'].value_counts()
    outlier_cluster_ids = cluster_counts[cluster_counts <= outlier_threshold].index.tolist()
    main_cluster_ids = cluster_counts[cluster_counts > outlier_threshold].index.tolist()

    df_outliers = df_clusters[df_clusters['Supply_Chain_Regime_ID'].isin(outlier_cluster_ids)]
    df_main = df_clusters[df_clusters['Supply_Chain_Regime_ID'].isin(main_cluster_ids)]

    df_outliers.to_csv(output_outliers, index=False)
    df_main.to_csv(output_main_regimes, index=False)

    print(f"Ana rejimlere {len(df_main)} ülke başarıyla kaydedildi: {output_main_regimes}")


if __name__ == "__main__":
    parse_tax_havens()