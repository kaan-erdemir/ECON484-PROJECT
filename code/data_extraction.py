import requests
import pandas as pd
import time
import os


def fetch_imf_imts_real_data(reporter_iso3, partner_iso3, start_year, end_year):
    """
    Fetches real trade data using the latest IMF API v2 (IMTS) infrastructure.
    """
    print(f"Fetching data: {reporter_iso3} -> {partner_iso3} ({start_year}-{end_year})")

    base_url = "https://api.imf.org/external/sdmx/2.1/data/IMTS"
    dimensions = f"{reporter_iso3}.XG_FOB_USD.{partner_iso3}.A"
    url = f"{base_url}/{dimensions}"

    params = {"startPeriod": start_year, "endPeriod": end_year}
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)

        if response.status_code == 400:
            return pd.DataFrame()
        elif response.status_code == 404:
            return pd.DataFrame()

        response.raise_for_status()
        data = response.json()

        series_list = data.get('dataSets', [{}])[0].get('series', {})
        if not series_list:
            return pd.DataFrame()

        series_key = list(series_list.keys())[0]
        observations = series_list[series_key].get('observations', {})

        if not observations:
            return pd.DataFrame()

        structure_dimensions = data.get('structure', {}).get('dimensions', {}).get('observation', [])
        time_periods = []
        for dim in structure_dimensions:
            if dim.get('id') == 'TIME_PERIOD':
                time_periods = [value.get('id') for value in dim.get('values', [])]

        records = []
        for obs_index, obs_values in observations.items():
            year_idx = int(obs_index)
            year = time_periods[year_idx] if year_idx < len(time_periods) else None
            export_val = float(obs_values[0]) if obs_values else None

            if year:
                records.append({
                    "Reporter": reporter_iso3,
                    "Partner": partner_iso3,
                    "Year": year,
                    "Export_Value_USD": export_val
                })

        return pd.DataFrame(records)

    except Exception as e:
        print(f"Error ({reporter_iso3}-{partner_iso3}): {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    print("--- Iteration 02: Real Data Fetching (New IMF API v2) Starting ---\n")

    START_YEAR = "2015"
    END_YEAR = "2023"

    reporters = ["USA", "CHN", "DEU", "JPN", "GBR", "FRA", "IND"]
    partners = ["CHN", "DEU", "MEX", "CAN", "RUS", "USA", "JPN"]

    all_dfs = []

    for reporter in reporters:
        for partner in partners:
            if reporter == partner:
                continue

            df = fetch_imf_imts_real_data(reporter_iso3=reporter, partner_iso3=partner, start_year=START_YEAR,
                                          end_year=END_YEAR)

            if df is not None and not df.empty:
                all_dfs.append(df)
            time.sleep(1.5)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        target_dir = os.path.join(project_root, 'original_data')

        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, 'imf_dots_sample.csv')

        try:
            final_df.to_csv(file_path, index=False)
            print("\n" + "=" * 50)
            print(f"[SUCCESS] Real IMF Data Downloaded and Saved Successfully!")
            print(f"Total Row Count: {len(final_df)}")
            print("=" * 50)
        except Exception as e:
            print(f"\n[ERROR] Could not save the file: {e}")
    else:
        print("\n[ERROR] No data could be fetched from IMF API.")