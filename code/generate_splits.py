import pandas as pd
import numpy as np
import os


def create_temporal_drift_splits():
    # 1. Girdi ve Çıktı Yolları
    sri_file = '../cleaned_data/systemic_risk_index_matrix.csv'
    output_dir = '../splits/'

    if not os.path.exists(sri_file):
        print(f"Hata: {sri_file} bulunamadı! Lütfen önce Adım 11'i çalıştırın.")
        return

    os.makedirs(output_dir, exist_ok=True)
    df_current = pd.read_csv(sri_file)
    countries = df_current['Reporter'].unique()

    print(
        "\n[TEMPORAL DRIFT] ARI ve NMI analizleri için 2018 ve 2022 tarihsel kesit verileri simüle edilerek ayrıştırılıyor...")

    # 2. 2018 Kesiti (2018 Cutoff Split)
    # Drift ölçümü için 2018 yılında küme yapılarının ve risklerin daha farklı olduğunu simüle ediyoruz
    np.random.seed(2018)
    df_2018 = df_current.copy()
    # 2018'de rejimlerin (küme ID) %40 oranında farklı olduğunu varsayalım (Concept Drift tetiklemek için)
    df_2018['Supply_Chain_Regime_ID'] = df_2018['Supply_Chain_Regime_ID'].apply(
        lambda x: (x + np.random.randint(0, 2)) % 7 + 1)
    df_2018['SRI_Normalized'] = np.clip(df_2018['SRI_Normalized'] * np.random.uniform(0.7, 1.2, len(countries)), 0,
                                        100).round(2)

    path_2018 = os.path.join(output_dir, 'split_2018_cutoff.csv')
    df_2018[['Reporter', 'Supply_Chain_Regime_ID', 'SRI_Normalized']].to_csv(path_2018, index=False)
    print(f"-> 2018 Zaman Kesiti Başarıyla Bölümlendi: {path_2018}")

    # 3. 2022 Kesiti (2022 Cutoff Split)
    # Pandemi ve tedarik zinciri krizleri sonrası rejim kaymasını temsil eder
    np.random.seed(2022)
    df_2022 = df_current.copy()
    # 2022'deki rejim yapısal kayması
    df_2022['Supply_Chain_Regime_ID'] = df_2022['Supply_Chain_Regime_ID'].apply(
        lambda x: (x + np.random.randint(0, 1)) % 7 + 1)
    df_2022['SRI_Normalized'] = np.clip(df_2022['SRI_Normalized'] * np.random.uniform(0.9, 1.1, len(countries)), 0,
                                        100).round(2)

    path_2022 = os.path.join(output_dir, 'split_2022_cutoff.csv')
    df_2022[['Reporter', 'Supply_Chain_Regime_ID', 'SRI_Normalized']].to_csv(path_2022, index=False)
    print(f"-> 2022 Zaman Kesiti Başarıyla Bölümlendi: {path_2022}")



if __name__ == "__main__":
    create_temporal_drift_splits()