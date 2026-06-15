# International Trade Networks and Supply Chain Vulnerability

## 1. Research Question
Global trade does not operate as a random collection of transactions; it functions within distinct, systemic regimes. This project utilizes machine learning to discover these hidden "Supply Chain Regimes" and evaluates whether the systematic misalignments between these data-driven clusters and countries' external vulnerability metrics can be leveraged to predict future balance-of-payments or supply chain shocks.

### Mathematical Formulation ($y = f(x)$)
The problem is structured as a two-stage unsupervised learning and alignment analysis task:

**Stage 1: Supply Chain Regime Discovery (Unsupervised Clustering)**
$$C = f(X_{\text{trade}})$$

* **Inputs ($X_{\text{trade}}$):** High-dimensional feature matrix containing country-level bilateral macro export and import volumes spanning historical vectors.
* **ML Task:** Unsupervised Clustering.
* **Output ($C$):** Categorical vector of discrete cluster assignments representing the natural "Supply Chain Regime" for each economy.

**Stage 2: Vulnerability Alignment Analysis**
$$\Delta = g(C, V_{\text{macro}})$$

* **Inputs ($V_{\text{macro}}$):** Independent macroeconomic external vulnerability metrics (Debt-to-GDP ratios, Current Account Deficit-to-GDP ratios, Sovereign Credit Ratings).
* **Output ($\\Delta$):** Structural misalignment matrix calculated via cross-tabulation and distance-to-centroid deviations, serving as an early-warning signal for future economic or supply shocks ($Y_{\text{shock}}$).

---

## 2. Input Data Description
* **Origin:** IMF Direction of Trade Statistics (DOTS) API, covering aggregate macro-level global direct bilateral trade flows. (Note: UN Comtrade API was scoped out during development to mitigate hyper-sparsity and maintain strict macroeconomic regime boundaries).
* **Key Fields / Columns:**
  * `Reporter`: ISO country identifiers for reporting economies.
  * `Partner`: ISO country identifiers for counterparty destination economies.
  * `Year`: Annual temporal tracker (2015-2023).
  * `Export_Value_USD_Scaled`: Log-transformed and standardized financial volume of the specific trade flow.
* **Known Data Issues:** Asymmetric reporting anomalies (e.g., Country A reports exporting $10M to Country B, but Country B reports importing $12M from Country A).

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
  * *Validation Metrics:* Silhouette Score and Qualitative Boundary Assessment.
* **Primary Model:** **Agglomerative Hierarchical Clustering**. This method is selected because trade blocs possess inherent nested structures (e.g., regional trade pacts operating inside global networks) which are best captured via Dendrogram analysis.
  * *Distance Metrics to Evaluate:* Euclidean, Manhattan, and Cosine distances.
  * *Linkage Criteria:* Ward's linkage (variance minimization) and Complete linkage.
  * *Validation Metric:* Cophenetic Correlation Coefficient to evaluate how faithfully the dendrogram preserves pairwise historical distances.

---

## 5. Expected Outputs & Interpretation
1. **Discrete Cluster IDs:** Categorical regime assignments for each economy (e.g., "Isolated Hegemon Sink", "The Industrial Production Engines", "Balanced Regional Hubs").
2. **Dendrogram Visualizations:** Tree diagrams highlighting the exact thresholds where regional trade agreements merge into broader geopolitical economic blocs.
3. **Misalignment Scores ($\Delta$):** Deviation rankings highlighting countries with high discrepancies between trade network resilience and sovereign default risk.

---

## 6. Risks & Drift to Watch For
* **Concept / Policy Drift:** Geopolitical fracturing alters static trade relationships over time. This project explicitly analyzes two structural breaks:
  1. **2018 (The US-China Tariff Escalation):** Marks the shift from peak global integration to protectionist decoupling.
  2. **2022 (The Russia-Ukraine War & Post-COVID Bottlenecks):** Marks the acceleration of "friend-shoring" and the weaponization of commodity supply chains.
  * *Quantification:* Models will be trained on pre-2018 data, projected onto 2022 data, and evaluated using the **Adjusted Rand Index (ARI)** and **Normalized Mutual Information (NMI)**. A sharp decline in ARI validates the presence of structural policy drift.
* **Statistical Risks:** High-dimensional trade matrices introduce the "Curse of Dimensionality", which can homogenize Euclidean distances. K-Means also assumes spherical cluster geometry, which fails to capture the elongated, corridor topology of global supply chains.

---

## 7. Specific Notes & Preprocessing Pipeline
* **Prior Quality Checks:** Missing value checks and distribution skewness testing across macro trade lines.
* **Data Transformations:** Trade volumes are heavily right-skewed; a $\log(1 + x)$ transformation will be applied to normalize data while preserving zero-trade matrices. All features will be scaled using `StandardScaler` to prevent extreme baseline variances from mathematically overwhelming the distance metrics.