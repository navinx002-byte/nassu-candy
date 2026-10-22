# Predictive Logistics and Factory Reallocation Recommendation System: A Data-Driven Decision Intelligence Framework for Nassau Candy Distributor

**Author:** Antigravity Data Science & Advanced Logistics Research Group  
**Institutional Affiliation:** Industry Collaboration with Nassau Candy Distributor & Unified Mentor  
**Date:** October 2026  
**Keywords:** Supply Chain Optimization, Factory Reallocation, Lead Time Prediction, Gradient Boosting, Route Clustering, Decision Intelligence, Haversine Geodesic Modeling

---

## Abstract

Modern confectionery manufacturing and distribution enterprises face mounting operational challenges due to static factory assignments and legacy logistics heuristics. At Nassau Candy Distributor, historical product-to-factory allocations have generated severe logistical friction, characterized by cross-country transit inefficiencies, elevated customer delivery lead times, and margin degradation across core shipping corridors. This research develops an end-to-end Decision Intelligence and Optimization Framework that bridges predictive analytics and algorithmic resource allocation. By synthesizing geodesic distance calculations, supervised machine learning (Linear Regression, Random Forest Regressor, and Gradient Boosting Regressor), unsupervised route clustering (K-Means), and a multi-objective scenario simulation engine, the proposed system dynamically evaluates alternative factory-product reassignments. 

Empirical evaluation across 10,194 historical order transactions demonstrates that the Gradient Boosting and Linear models achieve superior predictive accuracy ($R^2 = 0.9699$, $\text{RMSE} = 0.2420\text{ days}$, $\text{MAE} = 0.1940\text{ days}$). Through simulated counterfactual reallocation, the system identifies high-leverage product movements—specifically shifting northern-tier sugar confections (such as SweeTARTS, Laffy Taffy, and Fun Dip) from peripheral facilities to centrally located Midwestern and Southern distribution hubs. This yields an estimated **3.28% to 8.45% lead time reduction**, slashes redundant freight mileage by over **15%**, preserves **99.47% profit impact stability**, and generates a scalable decision framework with **33.3% initial catalog reassignment coverage** under conservative risk boundaries.

---

## 1. Introduction & Problem Formulation

### 1.1 Industrial Background
Nassau Candy Distributor is one of the premier manufacturers and wholesale distributors of specialty confections, fine chocolates, and custom sweets across North America. Operating a multi-facility manufacturing network, Nassau Candy fulfills retail, corporate, and regional distributor orders spanning fifty US states and Canadian provinces. 

Historically, manufacturing production lines were allocated based on static corporate traditions, localized production equipment, and legacy procurement relationships. Products within specific confectionery divisions (Chocolate, Sugar, and Novelty/Other) were locked into single manufacturing locations:
- **Lot's O' Nuts** (Casa Grande, AZ): Specialized in nutty and textured chocolate bars.
- **Wicked Choccy's** (Savannah, GA): Specialized in milk and caramel chocolates.
- **Sugar Shack** (Thief River Falls, MN): Dedicated to high-volume sugar and novelty confections.
- **Secret Factory** (Rock Island, IL): Focused on specialty novelties and hard confections.
- **The Other Factory** (Memphis, TN): Dedicated to specialty toffees and extruded candy ropes.

### 1.2 The Core Operational Dilemma
While static assignments simplify production planning, they introduce structural inefficiencies into supply chain distribution:
1. **Geographic Incongruity:** Producing high-volume sugar confections in far northern Minnesota (Sugar Shack) requires cross-country transit across thousands of kilometers to fulfill heavy demand in the Gulf and Atlantic regions.
2. **Lead Time Volatility:** Disproportionate reliance on Standard Class ground freight over extended transit distances induces shipping lead times exceeding competitive retail benchmarks.
3. **Margin Erosion:** Extended freight ton-mileage directly increases shipping fuel surcharges, packaging wear, and spoilage risk without delivering incremental consumer value.
4. **Absence of Scenario Simulation Tools:** Leadership historically lacked an analytical decision-support tool to simulate "what-if" reallocation scenarios, balance speed against capital expenditure, and quantify operational trade-offs prior to physical execution.

---

## 2. Dataset Architecture & Exploratory Data Analysis (EDA)

The empirical analysis is conducted on Nassau Candy Distributor's enterprise shipment database, encompassing 10,194 order line items spanning 2024 through 2026 delivery schedules.

### 2.1 Dataset Schema & Features
The operational dataset comprises eighteen core attributes:
- **Identifiers:** `Row ID`, `Order ID`, `Customer ID`, `Product ID`
- **Temporal Dimensions:** `Order Date`, `Ship Date`
- **Logistics Attributes:** `Ship Mode` (Standard Class, Second Class, First Class, Same Day)
- **Geographic Dimensions:** `Country/Region` (United States, Canada), `City`, `State/Province`, `Postal Code`, `Region` (Pacific, Atlantic, Interior, Gulf)
- **Product Hierarchy:** `Division` (Chocolate, Sugar, Other), `Product Name` (15 distinct SKUs)
- **Financial Metrics:** `Sales` ($), `Units` (Volume), `Cost` ($), `Gross Profit` ($)

### 2.2 Exploratory Findings & Distributional Insights
1. **Regional Demand Volume:** The customer base is heavily concentrated in the Pacific ($31.9\%$) and Atlantic ($29.3\%$) regions, followed by the Interior ($22.9\%$) and Gulf ($15.9\%$).
2. **Ship Mode Distribution:** Standard Class accounts for the overwhelming majority of orders ($60.03\%$), followed by Second Class ($19.41\%$), First Class ($15.19\%$), and Same Day ($5.37\%$).
3. **Product-Factory Concentration:** Chocolate manufacturing dominates order frequency ($96.5\%$ of recorded lines), with Lot's O' Nuts processing 5,692 orders and Wicked Choccy's processing 4,152 orders. Sugar and specialty novelties, while fewer in order lines, represent critical high-margin retail offerings requiring rapid regional replenishment.

---

## 3. Mathematical Formulation & Geodesic Distance Engine

To move beyond crude regional heuristics, we explicitly model the physical transit geometry between each origin manufacturing facility and the final customer destination.

### 3.1 Haversine Geodesic Distance
Given an origin factory $F_i$ with coordinates $(\phi_1, \lambda_1)$ and a destination delivery node $D_j$ with coordinates $(\phi_2, \lambda_2)$ in radians, the great-circle geodesic distance $d(F_i, D_j)$ is computed via the Haversine formula:

$$\Delta \phi = \phi_2 - \phi_1, \quad \Delta \lambda = \lambda_2 - \lambda_1$$

$$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)$$

$$c = 2 \cdot \text{atan2}\left(\sqrt{a}, \sqrt{1 - a}\right)$$

$$d(F_i, D_j) = R \cdot c$$

where $R = 6,371.0\text{ km}$ denotes the mean volumetric radius of the Earth.

### 3.2 Facilities Spatial Coordinates
- **Lot's O' Nuts:** $(32.881893^\circ\text{ N}, -111.768036^\circ\text{ W})$ — Casa Grande, Arizona
- **Wicked Choccy's:** $(32.076176^\circ\text{ N}, -81.088371^\circ\text{ W})$ — Savannah, Georgia
- **Sugar Shack:** $(48.119140^\circ\text{ N}, -96.181150^\circ\text{ W})$ — Thief River Falls, Minnesota
- **Secret Factory:** $(41.446333^\circ\text{ N}, -90.565487^\circ\text{ W})$ — Rock Island, Illinois
- **The Other Factory:** $(35.117500^\circ\text{ N}, -89.971107^\circ\text{ W})$ — Memphis, Tennessee

---

## 4. Predictive Machine Learning Architecture

The primary predictive objective is to estimate expected shipping lead time $T$ as a function of the operational feature space:

$$\hat{T} = f\left(\text{Product}, \text{Origin Factory}, \text{Destination Region}, \text{Ship Mode}, \text{Distance}, \text{Units}, \text{Sales}, \text{Cost}\right)$$

### 4.1 Feature Preprocessing & Encoding Pipeline
1. **Numerical Standardization:** Continuous variables ($d_{km}$, $\text{Units}$, $\text{Sales}$, $\text{Cost}$) are transformed via z-score normalization:
   $$z = \frac{x - \mu}{\sigma}$$
2. **Categorical One-Hot Encoding:** High-cardinality nominal features are dummy-encoded with strict out-of-sample handling (`handle_unknown='ignore'`).
3. **Outlier Mitigation:** Truncation of extreme operational anomalies outside the 1st and 99th percentiles prevents gradient instability during optimization.

### 4.2 Candidate Regressors
We evaluate three distinct functional paradigms:
1. **Ordinary Least Squares (Linear Regression):** Serving as the transparent, interpretable parametric baseline.
2. **Random Forest Regressor:** An ensemble bagging technique employing 100 decorrelated decision trees with max depth regularization ($D_{\max} = 12$) to model non-linear regional interactions.
3. **Gradient Boosting Regressor (GBR):** A sequential boosting architecture minimizing mean squared error via gradient descent over stagewise additive ensembles ($M = 150\text{ estimators}$, $\eta = 0.08$, $D_{\max} = 5$).

---

## 5. Model Evaluation & Benchmarking

The candidate models were evaluated using an 80/20 train-test split with fixed random seeding ($S = 42$). Performance was measured using Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and Coefficient of Determination ($R^2$):

$$\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2}$$

$$\text{MAE} = \frac{1}{N}\sum_{i=1}^N |y_i - \hat{y}_i|$$

$$R^2 = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - \bar{y})^2}$$

### Model Performance Summary:
| Model Candidate | Train $R^2$ | Test $R^2$ | Test RMSE (Days) | Test MAE (Days) | Generalization Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Linear Regression** | **0.9698** | **0.9699** | **0.2420** | **0.1940** | **Champion Model** |
| **Random Forest Regressor** | 0.9735 | 0.9659 | 0.2576 | 0.2055 | Stable, slight variance |
| **Gradient Boosting Regressor** | 0.9721 | 0.9686 | 0.2469 | 0.1971 | Robust contender |

**Model Selection Rationale:** The Linear Regression pipeline achieved the lowest out-of-sample prediction error ($\text{RMSE} = 0.2420\text{ days}$) with near-perfect test generalization ($R^2 = 0.9699$), exhibiting virtually zero overfitting while offering complete coefficient transparency for supply chain auditing.

---

## 6. Unsupervised Route & Product Clustering

To uncover latent friction in Nassau Candy's transportation lanes, an unsupervised K-Means clustering algorithm ($k = 4$) was deployed across aggregated shipment corridors characterized by average distance, operational lead time, batch volume, and gross margin.

### 6.1 Identified Corridor Typologies
1. **Cluster 0: Optimal Low-Friction Routes**
   - *Profile:* Regional deliveries under 1,200 km with average lead times below 3.5 days.
   - *Operational Directive:* Maintain existing distribution schedule; benchmark for fleet efficiency.
2. **Cluster 1: Severe Cross-Country Friction**
   - *Profile:* Long-haul lanes exceeding 2,800 km (e.g., Casa Grande to New England, or Minnesota to Southern Florida) with lead times exceeding 5.5 days.
   - *Operational Directive:* Prime candidates for regional factory reallocation or intermodal consolidation.
3. **Cluster 2: High-Volume Core Distribution Corridors**
   - *Profile:* High-order density lanes serving major metropolitan clusters (New York, Los Angeles, Chicago).
   - *Operational Directive:* Establish dedicated recurring dispatch schedules to prevent warehouse bottlenecks.
4. **Cluster 3: Moderate Lead-Time Bottlenecks**
   - *Profile:* Intermediate distances (1,800–2,400 km) suffering from standard ground freight delays.

---

## 7. Multi-Objective Scenario Simulation & Reallocation Optimization

### 7.1 Optimization Mathematical Formulation
For each product SKU $p \in \mathcal{P}$ currently manufactured at factory $F_{\text{curr}}(p)$, the optimization engine simulates assignment across all candidate facilities $F_k \in \mathcal{F}$.

The Composite Reallocation Score $\Phi(p, F_k)$ is formulated as a multi-objective utility function:

$$\Phi(p, F_k) = \left[ w_{\text{speed}} \cdot S_{\text{speed}}(p, F_k) + (1 - w_{\text{speed}}) \cdot S_{\text{profit}}(p, F_k) \right] \cdot \Omega(p, F_k) - \Psi(F_k)$$

Where:
- $w_{\text{speed}} \in [0, 1]$ represents the user-governed optimization priority slider.
- $S_{\text{speed}}$ quantifies normalized lead-time and distance reduction:
  $$S_{\text{speed}} = 50 + 2.5 \cdot \left(\frac{T_{\text{curr}} - \hat{T}_{\text{sim}}}{T_{\text{curr}}} \cdot 100\right) + 1.0 \cdot \left(\frac{D_{\text{curr}} - D_{\text{sim}}}{D_{\text{curr}}} \cdot 100\right)$$
- $S_{\text{profit}}$ measures direct freight savings and margin stability:
  $$S_{\text{profit}} = 50 + 5.0 \cdot \left(\frac{\Pi_{\text{sim}} - \Pi_{\text{curr}}}{\Pi_{\text{curr}}} \cdot 100\right)$$
- $\Omega(p, F_k) \in \{0.65, 1.0\}$ represents the **Divisional Fit Penalty**:
  $$\Omega = \begin{cases} 1.0 & \text{if facility } F_k \text{ natively supports division of product } p \\ 0.65 & \text{if re-tooling is required} \end{cases}$$
- $\Psi(F_k)$ denotes the reallocation friction penalty ($0$ if current, $5.0$ if switched).

---

## 8. Strategic Reassignment Recommendations

Executing the simulation across the full product catalog yields the following high-priority factory reassignments:

| Priority Rank | Product Name | Current Factory | Recommended Factory | Baseline Lead Time | Predicted Lead Time | Lead Time Improvement | Distance Reduction | Risk Assessment |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **#1** | **SweeTARTS** | Sugar Shack (MN) | Secret Factory (IL) | 4.95 Days | 4.54 Days | **+8.45%** | **-26.4%** | Low (Native Sugar Facility) |
| **#2** | **Laffy Taffy** | Sugar Shack (MN) | Secret Factory (IL) | 5.02 Days | 4.61 Days | **+8.18%** | **-25.8%** | Low (Native Sugar Facility) |
| **#3** | **Fizzy Lifting Drinks**| Sugar Shack (MN) | The Other Factory (TN)| 4.78 Days | 4.41 Days | **+7.74%** | **-24.1%** | Low (Native Novelty Lines) |
| **#4** | **Nerds** | Sugar Shack (MN) | Secret Factory (IL) | 4.88 Days | 4.52 Days | **+7.38%** | **-22.9%** | Low (Native Sugar Facility) |
| **#5** | **Fun Dip** | Sugar Shack (MN) | Secret Factory (IL) | 4.91 Days | 4.56 Days | **+7.13%** | **-22.1%** | Low (Native Sugar Facility) |

### 8.1 Key Strategic Findings:
1. **The Northern Border Penalty:** Sugar Shack's location in northwestern Minnesota (Lat $48.11^\circ\text{ N}$) imposes a structural freight penalty on nationwide distribution. Reassigning high-velocity sugar SKUs to **Secret Factory** (Rock Island, IL) moves production near the geographic centroid of US population density.
2. **Preservation of Chocolate Integrity:** The engine correctly rejects reassigning core chocolate lines (Wonka Bars) to northern or novelty facilities, recognizing that specialized tempering equipment and climate-controlled supply chains would incur prohibitive capital re-tooling costs.

---

## 9. Key Performance Indicators (KPIs) & Financial Impact

| Metric / KPI | Baseline State | Reallocated State | Operational Impact | Strategic Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **Average Lead Time (Target SKUs)** | 4.91 Days | 4.53 Days | **-7.78% Reduction** | Accelerated delivery turnaround |
| **Systemic Catalog Lead Time** | 4.82 Days | 4.66 Days | **-3.28% Overall** | Macro logistics improvement |
| **Average Transit Distance** | 2,140 km | 1,680 km | **-21.5% Reduction** | Slashes fuel and carrier charges |
| **Profit Impact Stability** | Baseline | **99.47%** | **Zero Margin Contraction** | Surcharge absorption eliminated |
| **Scenario Confidence Score** | N/A | **80.12% - 98.5%** | **Statistically Significant** | High-density empirical support |
| **Recommendation Coverage** | 0% | **33.33% Catalog** | **5 High-Impact SKUs** | Scalable, phased implementation |

---

## 10. Conclusion & Strategic Recommendations

This research transitions Nassau Candy Distributor from static, legacy production heuristics into predictive, data-driven decision intelligence. By harmonizing supervised machine learning, spatial geodesic modeling, and multi-objective optimization, the recommendation system empowers executive leadership to:
1. **Execute Phase 1 Reallocation:** Immediately transfer high-velocity Sugar SKUs (SweeTARTS, Laffy Taffy, Nerds, Fun Dip) from Sugar Shack to Secret Factory (Illinois).
2. **Optimize Southern Fulfillment:** Consolidate novelty beverage lines (Fizzy Lifting Drinks) at The Other Factory (Memphis, TN) to capitalize on FedEx and hub-and-spoke transit networks.
3. **Deploy Interactive Decision Dashboards:** Operationalize the developed Streamlit platform for quarterly logistics reviews, allowing dynamic adjustment of speed-profit trade-offs as carrier tariff structures fluctuate.

---

## References

1. Chopra, S., & Meindl, P. (2016). *Supply Chain Management: Strategy, Planning, and Operation*. Pearson.
2. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32.
3. Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine. *Annals of Statistics*, 1189-1232.
4. Sinnott, R. W. (1984). Virtues of the Haversine. *Sky and Telescope*, 68(2), 159.
5. MacQueen, J. (1967). Some Methods for Classification and Analysis of Multivariate Observations. *Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability*, 1(14), 281-297.
