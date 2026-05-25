# International Trade Networks and Supply Chain Vulnerability

## 1. Research Question
Global trade does not operate as a random collection of transactions; it functions within distinct, systemic regimes. This project utilizes machine learning to discover these hidden "Supply Chain Regimes" and evaluates whether the systematic misalignments between these data-driven clusters and countries' external vulnerability metrics can be leveraged to predict future balance-of-payments or supply chain shocks.

### Mathematical Formulation ($y = f(x)$)
The problem is structured as a two-stage unsupervised learning and alignment analysis task:

**Stage 1: Supply Chain Regime Discovery (Unsupervised Clustering)**
$$C = f(X_{\text{trade}})$$

* **Inputs ($X_{\text{trade}}$):** High-dimensional feature matrix containing country-level import/export dependency matrices, commodity concentrations (Herfindahl-Hirschman Index), and weighted tariff structures.
* **ML Task:** Unsupervised Clustering.
* **Output ($C$):** Categorical vector of discrete cluster assignments representing the natural "Supply Chain Regime" for each economy.

**Stage 2: Vulnerability Alignment Analysis**
$$\Delta = g(C, V_{\text{macro}})$$

* **Inputs ($V_{\text{macro}}$):** Independent macroeconomic external vulnerability metrics (Debt-to-GDP ratios, Current Account Deficit-to-GDP ratios, Sovereign Credit Ratings).
* **Output ($\Delta$):** Structural misalignment matrix calculated via cross-tabulation and distance-to-centroid deviations, serving as an early-warning signal for future economic or supply shocks ($Y_{\text{shock}}$).

---

## 2. Input Data Description
* **Origin:** UN Comtrade API (covering global direct bilateral trade flows) supplemented by the IMF Direction of Trade Statistics (DOTS).
* **Key Fields / Columns:**
  * `Reporter_Code` / `Partner_Code`: ISO country identifiers.
  * `Commodity_Code`: HS (Harmonized System) 2-digit or 4-digit product classifications.
  * `Trade_Value_USD`: Total annual financial volume of the specific trade flow.
  * `Tariff_Structure`: Effectively applied weighted average tariff rates per country pair.
* **Known Data Issues:** * Asymmetric reporting anomalies (e.g., Country A reports exporting $10M to Country B, but Country B reports importing $12M from Country A).
  * Extreme zero-inflation and matrix sparsity due to the absence of direct trading relationships between smaller economies.

---

## 3. Verification & Validation (V&V) Data Description
* **Origin:** Bloomberg Sovereign Rating Database (historical S&P, Moody's, and Fitch ratings) and the World Bank World Development Indicators (WDI).
* **Key Fields / Columns:**
  * `Sovereign_Rating`: Categorical credit risk tiers mapped to a standardized numerical scale (e.g., AAA = 22, C = 1).
  * `Debt_to_GDP_Ratio`: Gross government debt expressed as a percentage of national GDP.
  * `Current_Account_Deficit_to_GDP`: External financing vulnerability proxy metric.
* **V&V Methodology (Alignment Analysis):** We will implement an Alignment Analysis utilizing a **Cross-Tabulation Matrix**. By mapping our data-driven trade clusters ($C$) against independent sovereign credit risk tiers ($V_{\text{macro}}$), we will identify statistical anomalies—countries whose secure trade networks mask poor macroeconomic books, or conversely, fiscally sound nations embedded within highly fragile, hyper-dependent supply lines.

---

## 4. Methods to Be Used
* **Baseline Model:** Principal Component Analysis (PCA) for dimensionality reduction, followed by **K-Means Clustering**.
  * *Validation Metrics:* Silhouette Score and the Elbow Method (Within-Cluster Sum of Squares).
* **Primary Model:** **Agglomerative Hierarchical Clustering**. This method is selected because trade blocs possess inherent nested structures (e.g., regional trade pacts operating inside global networks) which are best captured via Dendrogram analysis.
  * *Distance Metrics to Evaluate:* Euclidean, Manhattan, and Cosine distances.
  * *Linkage Criteria:* Ward's linkage (variance minimization) and Complete linkage.
  * *Validation Metric:* Cophenetic Correlation Coefficient to evaluate how faithfully the dendrogram preserves pairwise historical distances.

---

## 5. Expected Outputs & Interpretation
1. **Discrete Cluster IDs:** Categorical regime assignments for each economy (e.g., "High-Tech Component Hubs", "Primary Commodity Exporters", "Tax Haven Nodes").
2. **Dendrogram Visualizations:** Tree diagrams highlighting the exact thresholds where regional trade agreements merge into broader geopolitical economic blocs.
3. **Misalignment Scores ($\Delta$):** Deviation rankings highlighting countries with high discrepancies between trade network resilience and sovereign default risk.

---

## 6. Risks & Drift to Watch For
* **Concept / Policy Drift:** Geopolitical fracturing alters static trade relationships over time. This project explicitly analyzes two structural breaks:
  1. **2018 (The US-China Tariff Escalation):** Marks the shift from peak global integration to protectionist decoupling.
  2. **2022 (The Russia-Ukraine War & Post-COVID Bottlenecks):** Marks the acceleration of "friend-shoring" and the weaponization of commodity supply chains.
  * *Quantification:* Models will be trained on pre-2018 data, projected onto 2022 data, and evaluated using the **Adjusted Rand Index (ARI)** and **Normalized Mutual Information (NMI)**. A sharp decline in ARI validates the presence of structural policy drift.
* **Statistical Risks:** High-dimensional trade matrices introduce the "Curse of Dimensionality", which can homogenize Euclidean distances. K-Means also assumes spherical cluster geometry, which fails to capture the elongated, hub-and-spoke topology of global supply chains.

---

## 7. Specific Notes & Preprocessing Pipeline
* **Prior Quality Checks:** Missing value heatmaps and distribution skewness testing across commodity trades.
* **Data Transformations:** Trade volumes are heavily right-skewed; a $\log(1 + x)$ transformation will be applied to normalize data while preserving zero-trade matrices. All features will be scaled using `StandardScaler` or `MinMaxScaler` to prevent high-value primary commodities (like crude oil) from mathematically overwhelming low-volume but highly critical components (like semiconductor machinery).
