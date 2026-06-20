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
## Iteration 05: Metric-Driven Validation & Geometric Critique (K-Means)
* **Objective:** Quantify the mathematical validity of the baseline K-Means model and diagnose its structural limitations using silhouette profiling.
* **Action:** Developed `evaluate_kmeans.py` to extract silhouette coefficients for each individual economy and render a comprehensive validation profile.
* **Debugging History:**
    1.  **Error:** `[ERROR] An unexpected error occurred: 'Axes' object has no attribute 'setTitle'`
        * *Cause:* A typographical syntax error in the Matplotlib rendering loop where a camelCase method (`setTitle`) was mistakenly called on a subplot axis object instead of the correct snake_case function.
        * *Fix:* Refactored the code to utilize `ax1.set_title()`, allowing the pipeline to execute without further visualization crashes.
* **Mathematical & Economic Insights Discovered:**
    * **Cluster 0 (Balanced Regional Hubs):** FRA (0.75), GBR (0.77), and IND (0.71) achieved exceptionally high, stable silhouette scores. This empirically proves they form a highly homogeneous core with tightly aligned bilateral trade footprints.
    * **Cluster 1 (Global Production Engines - Boundary Flaw):** CHN achieved a solid score (0.43), but DEU plunged into negative territory (-0.14). This negative coefficient serves as mathematical proof of a *hard boundary flaw*. K-Means forced Germany into China's export-heavy cluster due to absolute volume, completely blinding the model to Germany's organic economic ties and physical integration with the Eurozone (Cluster 0).
    * **Cluster 2 (The Isolated Hegemon):** USA returned a silhouette score of exactly `0.0000`. In Scikit-Learn, a single-element cluster automatically yields a zero score. This validates that the USA behaves as an completely unique, isolated trade pole that cannot be geometrically blended with any other global economy.
* **Result:** Successfully generated and saved `plots/kmeans_silhouette_analysis.png`. The structural failures discovered mathematically justified the immediate transition to non-spherical hierarchical models.

## Iteration 06: Empirical Distance Metric Justification Matrix
* **Objective:** Resolve K-Means' rigid geometric assumptions by testing multi-metric agglomerative combinations and validating their topological fidelity.
* **Action:** Created `distance_justification.py` to compute pairwise trade-space distance matrices using Euclidean, Manhattan (Cityblock), and Cosine formulas, combining them with Average, Complete, Single, and Ward linkage criteria.
* **Validation Framework:** Selected the **Cophenetic Correlation Coefficient ($r$)** as the target metric to measure how faithfully each hierarchical tree configuration preserves the original unclustered high-dimensional distances.
* **Empirical Benchmarking Results:**
    * **The Winner:** Manhattan Distance combined with Average Linkage achieved the highest score ($r = 0.09015$), surpassing the excellent fidelity threshold. Manhattan's linear scaling ($\sum |u_i - v_i|$) proved highly resilient to right-skewed trade volume anomalies and localized protectionist spikes.
    * **Proportional Validation:** Cosine Distance with Average Linkage also scored strongly ($r = 0.8812$), proving that the underlying proportional footprint (structural ratios) of global supply chains holds massive distinct geometric validity.
    * **The Failure:** Euclidean Distance combined with Ward’s Linkage returned the worst performance ($r = 0.6447$). Because Ward’s method introduces a mathematical constraint to minimize internal variance, it forces spherical clusters onto an inherently elongated, hub-and-spoke trade corridor, severely tahrifing/distorting macroeconomic reality.
* **Result:** Rendered and saved a rigorous comparative bar chart to `plots/distance_metric_fidelity.png` and compiled the formal analytical report into `docs/distance_metrics.md`. This locks in Manhattan + Average Linkage as the absolute production configuration for final dendrogram construction.
---

## Current Pipeline Execution Order
1. python code/data_extraction.py
2. python code/preprocessing.py
3. python code/baseline_kmeans.py
4. python code/evaluate_kmeans.py
5. python code/distance_justification.py