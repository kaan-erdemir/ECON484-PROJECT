## Overview
This document serves as a historical record of the AI-assisted development process for the "Global Supply Chain Regimes" clustering project. It tracks the pipeline iterations, engineering decisions, errors encountered, and debugging steps from project inception to the successful execution of the baseline machine learning model.

---

## Iteration 01: Project Architecture & Ledger
* **Objective:** Prevent version control chaos and separate raw data from code.
* **Action:** Established a professional data science directory structure (`code/`, `original_data/`, `cleaned_data/`, `plots/`, `ai_prompts/`).
* **Action:** Created a `ledger.csv` file to act as an immutable audit log, tracking the status of each pipeline component (Planned vs. Completed).

## Iteration 02: Real Data Extraction (IMF API v2)
* **Objective:** Fetch real-world macroeconomic trade data to feed the clustering models.
* **Action:** Wrote `data_extraction.py` to pull unmanipulated export data from the new IMF API infrastructure.
* **Critical Fix:** Initially, the script was configured to pull data *only* for the USA. This caused mathematical failures in the machine learning phase (PCA requires more samples than dimensions). The script was refactored to fetch a matrix of 7 major economies (USA, CHN, DEU, JPN, GBR, FRA, IND) and their top trading partners.

## Iteration 03: Preprocessing Pipeline
* **Objective:** Prepare raw data for distance-based machine learning algorithms (K-Means).
* **Action:** Developed `preprocessing.py` to handle the data transformation.
* **Techniques Applied:** * Filled missing values (`NaN`) with 0 to prevent algorithmic crashes.
    * Applied logarithmic transformation (`Log(1+x)`) to compress extreme trade volumes (e.g., billions of dollars vs. thousands of dollars).
    * Scaled the data using `StandardScaler` to ensure fair feature weighting.
* **Result:** Successfully reduced the skewness of the export values from `0.22` to `-1.31`, perfectly stabilizing the dataset.

## Iteration 04: Machine Learning (Baseline PCA & K-Means)
* **Objective:** Reduce dimensionality and cluster the countries into Supply Chain Regimes.
* **Action:** Created `baseline_kmeans.py`. Decided to use a pure Python script (`.py`) instead of Jupyter Notebook (`.ipynb`) to maintain full automation of the data pipeline.
* **Debugging History:**
    1.  **Error:** `n_components=2 must be between 0 and min(n_samples, n_features)=1`
        * *Cause:* Feature matrix shape was `(1, 45)` because only USA data was processed.
        * *Fix:* Executed a hard reset on the pipeline, deleted old CSVs, and re-ran the updated `data_extraction.py` to include 7 countries.
    2.  **Error:** `ModuleNotFoundError: No module named 'code.data_extraction'`
        * *Cause:* Attempting to use Python `import` statements across pipeline scripts.
        * *Fix:* Enforced strict pipeline architecture. Scripts must not import each other; they must only communicate by reading/writing CSV files.
    3.  **Error:** `AttributeError: 'NoneType' object has no attribute 'empty'`
        * *Cause:* Mixed API extraction logic into the ML script by accident.
        * *Fix:* Completely wiped `baseline_kmeans.py` and rewrote it to exclusively contain Scikit-Learn logic.
* **Final Result:** Successfully generated a PCA-reduced scatter plot showing 3 distinct global supply chain regimes:
    * **Cluster 0 (Purple):** JPN, FRA, GBR, IND (Balanced trade patterns)
    * **Cluster 1 (Green):** CHN, DEU (Global production/export engines)
    * **Cluster 2 (Yellow):** USA (Isolated, distinct trade pole)
* **Refinement:** Corrected the file saving paths so that visualizations are directly routed to the `plots/` directory to maintain structural integrity.

---

## Current Pipeline Execution Order
To reproduce the data science pipeline from raw API extraction to final clustering plots, execute the following commands in order:

1. `python code/data_extraction.py`
2. `python code/preprocessing.py`
3. `python code/baseline_kmeans.py`