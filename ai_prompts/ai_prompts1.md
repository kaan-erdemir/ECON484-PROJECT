# AI Prompt History

This document contains a summary of interactions with Large Language Models (LLMs - Gemini) for architectural setup, debugging, and empirical model optimization during the "Global Supply Chain Regimes" clustering project. The prompts were designed following the "context, task, and format" framework to maximize the efficiency and accuracy of the AI's outputs.

## 1. Project Architecture and Pipeline Tracking
* **Prompt:** "I am starting a machine learning project to cluster global supply chain regimes. What is the industry best practice for structuring my directories to separate raw data, scripts, and visualizations? Additionally, how can I set up a simple `ledger.csv` to track pipeline milestones and prevent scope creep?"
* **Takeaway:** Understood the importance of isolated data science directories (`code/`, `cleaned_data/`, `plots/`) and successfully implemented an immutable audit log (ledger) to strictly track Planned vs. Completed pipeline components.

## 2. API Extraction and PCA Dimensionality Rules
* **Prompt:** "I am fetching trade data using the IMF API v2. However, my PCA dimensionality reduction is failing with an error indicating `n_components` must be between 0 and `min(n_samples, n_features)`. My current script only pulls data for the USA. How should I refactor the code to fetch a matrix of multiple major economies to satisfy PCA's mathematical requirements?"
* **Takeaway:** Grasped the mathematical relationship between sample size and dimensions in PCA. Successfully scaled the data extraction script to dynamically pull a matrix of 7 major global economies (USA, CHN, DEU, JPN, GBR, FRA, IND).

## 3. Data Preprocessing for Distance-Based ML
* **Prompt:** "The macroeconomic export data I fetched has extreme outliers (ranging from billions of dollars to a few thousands) and some missing values (`NaN`). What are the optimal preprocessing techniques in `pandas` and `scikit-learn` to stabilize this specific type of highly skewed financial data before feeding it into K-Means?"
* **Takeaway:** Learned how to safely handle sparsity by filling missing values with zero, and successfully applied logarithmic transformation (`Log(1+x)`) combined with `StandardScaler` to compress extreme trade volumes and remove skewness.

## 4. Script Isolation and Module Errors
* **Prompt:** "I am trying to run my `baseline_kmeans.py` script, but I am getting a `ModuleNotFoundError` when it tries to import variables from my `data_extraction.py` script. How can I resolve this dependency issue and enforce a strict, decoupled pipeline architecture where scripts run independently?"
* **Takeaway:** Grasped the concept of pipeline isolation. Refactored the architecture so that Python scripts do not import each other directly; instead, they communicate exclusively by reading and writing intermediate CSV files to the `cleaned_data/` directory.

## 5. Matplotlib Debugging and Geometric Interpretation
* **Prompt:** "I am plotting silhouette scores to validate my K-Means model, but Matplotlib throws this error: `'Axes' object has no attribute 'setTitle'`. How do I fix this syntax issue? Furthermore, the output shows Germany with a negative silhouette score (-0.1358). How do I interpret this mathematically and economically?"
* **Takeaway:** Resolved the camelCase vs. snake_case Matplotlib bug (using `set_title()`). Understood how to interpret negative silhouette coefficients as proof of K-Means' "hard boundary flaws," demonstrating that volume-based clustering incorrectly separated Germany from its organic Eurozone ties.

## 6. Empirical Benchmarking with Cophenetic Correlation
* **Prompt:** "I am transitioning to Agglomerative Hierarchical Clustering to solve K-Means' spherical limitations. How can I write a Python script that loops through different distance metrics (Euclidean, Manhattan, Cosine) and linkage methods, and uses the Cophenetic Correlation Coefficient ($r$) to empirically evaluate which combination best preserves the original trade topology?"
* **Takeaway:** Successfully implemented an automated empirical benchmarking matrix. Discovered and documented that Manhattan Distance combined with Average Linkage ($r=0.9015$) handles right-skewed trade volume anomalies vastly better than traditional Euclidean/Ward methods ($r=0.6447$).