import pandas as pd
import numpy as np
import os


def calculate_structural_misalignment():
    # 1. Dosya Yolları
    mapped_file = '../cleaned_data/country_vulnerability_mapped.csv'
    baseline_file = '../cleaned_data/regime_vulnerability_baselines.csv'
    output_misalignment_file = '../cleaned_data/structural_misalignment_results.csv'

    if not os.path.exists(mapped_file) or not os.path.exists(baseline_file):
        print("Hata: Gerekli girdi dosyaları bulunamadı! Lütfen önce Adım 9'u çalıştırın.")
        return

    # Verileri Yükle
    df_countries = pd.read_csv(mapped_file)
    df_baselines = pd.read_csv(baseline_file)

    # 2. Baseline Verilerini Kolay Eşleşme İçin Yeniden Adlandır ve Sözlüğe Çevir
    df_baselines = df_baselines.rename(columns={
        'Debt_to_GDP_Ratio': 'Base_Debt',
        'Current_Account_to_GDP_Ratio': 'Base_CA',
        'Sovereign_Credit_Score': 'Base_Credit'
    })

    # Ülke matrisine ait olduğu kümenin baseline değerlerini merge ile ekle
    df_analysis = pd.merge(df_countries,
                           df_baselines[['Supply_Chain_Regime_ID', 'Base_Debt', 'Base_CA', 'Base_Credit']],
                           on='Supply_Chain_Regime_ID', how='inner')

    # 3. Sapma (Misalignment) Hesaplama
    # Her gösterge için mutlak farkı buluyoruz
    df_analysis['Debt_Deviation'] = np.abs(df_analysis['Debt_to_GDP_Ratio'] - df_analysis['Base_Debt'])
    df_analysis['CA_Deviation'] = np.abs(df_analysis['Current_Account_to_GDP_Ratio'] - df_analysis['Base_CA'])
    df_analysis['Credit_Deviation'] = np.abs(df_analysis['Sovereign_Credit_Score'] - df_analysis['Base_Credit'])

    # Farkları normalize etmek için (Scale bağımsız hale getirmek için) her farkı kendi serisinin standart sapmasına bölüyoruz (Z-score yaklaşımı)
    # Eğer serideki tüm farklar aynıysa (örneğin az sayıda veri varken standart sapma 0 ise) bölme hatası olmaması için küçük bir epsilon ekliyoruz.
    def normalize_dev(series):
        std = series.std()
        return series / (std if std > 0 else 1.0)

    df_analysis['Norm_Debt_Dev'] = normalize_dev(df_analysis['Debt_Deviation'])
    df_analysis['Norm_CA_Dev'] = normalize_dev(df_analysis['CA_Deviation'])
    df_analysis['Norm_Credit_Dev'] = normalize_dev(df_analysis['Credit_Deviation'])

    # 4. Ağırlıklı Yapısal Sapma Skoru (Misalignment Score)
    # Borç, Cari Açık ve Kredi Notu sapmalarına eşit ağırlık (%33.3) veriyoruz
    w1, w2, w3 = 0.33, 0.33, 0.34
    df_analysis['Misalignment_Score'] = (
            w1 * df_analysis['Norm_Debt_Dev'] +
            w2 * df_analysis['Norm_CA_Dev'] +
            w3 * df_analysis['Norm_Credit_Dev']
    )

    # Sonuçları yuvarla ve Skora göre büyükten küçüğe sırala
    df_analysis = df_analysis.round(3)
    df_final = df_analysis.sort_values(by='Misalignment_Score', ascending=False)

    # İhtiyacımız olan sütunları seçip kaydet
    output_cols = [
        'Reporter', 'Supply_Chain_Regime_ID',
        'Debt_to_GDP_Ratio', 'Base_Debt',
        'Current_Account_to_GDP_Ratio', 'Base_CA',
        'Sovereign_Credit_Score', 'Base_Credit',
        'Misalignment_Score'
    ]
    df_final[output_cols].to_csv(output_misalignment_file, index=False)


if __name__ == "__main__":
    calculate_structural_misalignment()