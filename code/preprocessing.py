import os
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.compose import ColumnTransformer


def build_preprocessing_pipeline():
    """
    Builds a scikit-learn preprocessing pipeline that handles missing values,
    applies a log(1+x) transformation to address right-skewness, and scales features.
    """
    # 1. Log(1+x) transformer to handle heavy right-skewed trade data
    log1p_transformer = FunctionTransformer(np.log1p, validate=False)

    # 2. Pipeline for numerical features (Export_Value_USD)
    # Step A: Impute NaNs with 0 (Assuming missing trade data implies no reported trade)
    # Step B: Log Transformation
    # Step C: Standard Scaler to prevent large magnitudes from overwhelming distance metrics
    numeric_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=0.0)),
        ('log_transform', log1p_transformer),
        ('scaler', StandardScaler())
    ])

    # 3. ColumnTransformer to apply the pipeline to specific columns while keeping the rest
    preprocessor = ColumnTransformer(
        transformers=[
            ('trade_volume', numeric_pipeline, ['Export_Value_USD'])
        ],
        remainder='passthrough'  # Keep Reporter, Partner, Year unchanged
    )

    return preprocessor


if __name__ == "__main__":
    print("--- Iteration 03: Preprocessing Pipeline Starting ---\n")

    # Absolute path configurations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    input_path = os.path.join(project_root, 'original_data', 'imf_dots_sample.csv')
    output_dir = os.path.join(project_root, 'cleaned_data')
    output_path = os.path.join(output_dir, 'imf_dots_cleaned.csv')

    try:
        # Load the raw data
        print(f"Loading raw data from: {input_path}")
        df_raw = pd.read_csv(input_path)

        print("\n[Pre-Processing Stats]")
        print(f"Missing Values in Export_Value_USD: {df_raw['Export_Value_USD'].isna().sum()}")
        print(f"Raw Data Skewness: {df_raw['Export_Value_USD'].skew():.2f}")

        # Build and apply the pipeline
        print("\nApplying Imputation, Log(1+x) Transformation, and StandardScaler...")
        pipeline = build_preprocessing_pipeline()

        # Fit and transform the data
        transformed_data = pipeline.fit_transform(df_raw)

        # Reconstruct the DataFrame
        # Note: ColumnTransformer places transformed columns first, then 'passthrough' columns
        passthrough_cols = [col for col in df_raw.columns if col != 'Export_Value_USD']
        new_columns = ['Export_Value_USD_Scaled'] + passthrough_cols

        df_cleaned = pd.DataFrame(transformed_data, columns=new_columns)

        # Reorder columns to match original structure
        df_cleaned = df_cleaned[['Reporter', 'Partner', 'Year', 'Export_Value_USD_Scaled']]

        print("\n[Post-Processing Stats]")
        print(f"Missing Values in Export_Value_USD_Scaled: {df_cleaned['Export_Value_USD_Scaled'].isna().sum()}")
        print(f"Transformed Data Skewness: {df_cleaned['Export_Value_USD_Scaled'].skew():.2f}")

        # Save to cleaned_data directory
        os.makedirs(output_dir, exist_ok=True)
        df_cleaned.to_csv(output_path, index=False)

        print("\n" + "=" * 50)
        print(f"[SUCCESS] Data successfully cleaned, transformed, and scaled.")
        print(f"Saved to: {os.path.abspath(output_path)}")
        print("=" * 50)
        print("\nFirst 5 rows of cleaned data:")
        print(df_cleaned.head())
        print("\nNext Step: Iteration 04 - code/baseline_kmeans.ipynb")

    except FileNotFoundError:
        print(
            f"\n[ERROR] Raw data file not found at {input_path}. Please ensure Iteration 02 was completed successfully.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")