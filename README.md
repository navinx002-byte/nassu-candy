# 🍬 Nassau Candy Distributor: Factory Reallocation & Shipping Optimization Recommendation System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade Decision Intelligence Platform designed for **Nassau Candy Distributor** in collaboration with **Unified Mentor**. The system transitions logistics management from static legacy heuristics to predictive machine learning and multi-objective optimization—predicting shipping outcomes, reallocating products to optimal manufacturing hubs, and balancing delivery speed with profitability.

---

## 📌 Executive Summary & Scorecard

Nassau Candy currently assigns products to manufacturing facilities using legacy, static rules. This results in excessive cross-country freight distances, prolonged shipping lead times (up to 5–7 days for retail customers), and margin erosion from fuel surcharges.

This platform introduces **prescriptive decision intelligence** that evaluates counterfactual factory reassignments across 10,194 historical orders and provides ranked, actionable reallocation recommendations.

```
+-----------------------------------------------------------------------------------------+
|                                    EXECUTIVE KPI SCORECARD                              |
+-----------------------------------------------------------------------------------------+
|  KPI                           Baseline             Optimized Reallocation   Net Impact |
|  ---------------------------   ------------------   ----------------------   ---------- |
|  Lead Time Reduction (%)       --                   3.28% to 8.45%           -7.8% Avg  |
|  Average Shipping Distance     2,140 km             1,680 km                 -21.5%     |
|  Profit Impact Stability       100.0%               99.47%                   Protected  |
|  Scenario Confidence Score     --                   80.1% to 98.5%           High       |
|  Recommendation Coverage       0%                   33.3% (5 High-Impact)    Scalable   |
|  Annual Direct Freight Savings --                   $44.71k+ (Scaled Lane)   Direct ROI |
+-----------------------------------------------------------------------------------------+
```

---

## 🏭 Production Facilities & Network Coordinates

| Facility Name | Geographic Coordinates | Location | Specialization |
| :--- | :---: | :--- | :--- |
| **Lot's O' Nuts** | `32.881893, -111.768036` | Casa Grande, Arizona | Textured & Nutty Chocolate Confections |
| **Wicked Choccy's** | `32.076176, -81.088371` | Savannah, Georgia | Milk Chocolate & Caramel Confections |
| **Sugar Shack** | `48.119140, -96.181150` | Thief River Falls, Minnesota | High-Volume Sugar Candies |
| **Secret Factory** | `41.446333, -90.565487` | Rock Island, Illinois | Specialty Novelties & Hard Confections |
| **The Other Factory** | `35.117500, -89.971107` | Memphis, Tennessee | Toffees, Extruded Sweets & Logistics Hub |

---

## 🔬 Analytical Methodology & Machine Learning

### 1. Spatial Geodesic Distance Engine
Using the exact coordinates of Nassau Candy's five factories and destination customer locations across 59 US states and Canadian provinces, geodesic shipping distances are calculated via the Haversine formula:
$$d(F_i, D_j) = 2R \cdot \text{atan2}\left(\sqrt{\sin^2(\Delta \phi / 2) + \cos \phi_1 \cos \phi_2 \sin^2(\Delta \lambda / 2)}, \sqrt{1 - a}\right)$$

### 2. Supervised Regression Benchmarks
Three algorithms were trained to predict operational transit lead time given product division, origin factory, destination region, ship mode, units, sales, and distance:

| Model Architecture | Train $R^2$ | Test $R^2$ | Test RMSE (Days) | Test MAE (Days) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Linear Regression** | **0.9698** | **0.9699** | **0.2420** | **0.1940** | 🏆 **Champion Model** |
| **Gradient Boosting Regressor** | 0.9721 | 0.9686 | 0.2469 | 0.1971 | Robust Ensemble |
| **Random Forest Regressor** | 0.9735 | 0.9659 | 0.2576 | 0.2055 | Non-Linear Baseline |

### 3. Route & Product Clustering (K-Means)
Unsupervised clustering ($k = 4$) segmented delivery corridors into:
- **Optimal Low-Friction Routes:** Regional lanes under 1,200 km (lead times $< 3.5$ days).
- **High-Volume Core Arteries:** Major urban destinations (New York, Los Angeles, Chicago).
- **Severe Cross-Country Friction:** Peripheral cross-continental routes ($> 2,800$ km) with severe transit penalties.

---

## 🎯 Top-5 Algorithmic Reallocation Recommendations

| Rank | Product SKU | Current Factory | Recommended Factory | Baseline Lead Time | Optimized Lead Time | Lead Time Gain | Distance Reduction | Risk Assessment |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **#1** | **SweeTARTS** | Sugar Shack (MN) | Secret Factory (IL) | 4.95 Days | 4.54 Days | **+8.45%** | **-26.4%** | Low (Native Sugar Facility) |
| **#2** | **Laffy Taffy** | Sugar Shack (MN) | Secret Factory (IL) | 5.02 Days | 4.61 Days | **+8.18%** | **-25.8%** | Low (Native Sugar Facility) |
| **#3** | **Fizzy Lifting Drinks** | Sugar Shack (MN) | The Other Factory (TN) | 4.78 Days | 4.41 Days | **+7.74%** | **-24.1%** | Low (Native Novelty Line) |
| **#4** | **Nerds** | Sugar Shack (MN) | Secret Factory (IL) | 4.88 Days | 4.52 Days | **+7.38%** | **-22.9%** | Low (Native Sugar Facility) |
| **#5** | **Fun Dip** | Sugar Shack (MN) | Secret Factory (IL) | 4.91 Days | 4.56 Days | **+7.13%** | **-22.1%** | Low (Native Sugar Facility) |

---

## 🖥️ Streamlit Web Application Modules

The application includes six integrated analytics modules:
1. **Factory Optimization Simulator:** Select any SKU and evaluate simulated shipping lead times, freight distance shifts, and composite scores across all five candidate facilities.
2. **What-If Scenario Analysis:** Side-by-side comparison of baseline vs. recommended configurations, including a live custom reassignment tester.
3. **Recommendation Dashboard:** Ranked reallocation suggestions, efficiency gains, and one-click CSV export.
4. **Risk & Impact Panel:** Facility tooling mismatch alerts, chocolate line protection boundaries, and financial margin trade-off frontiers.
5. **Network & Route Clustering:** Geographic map of manufacturing facilities and interactive K-Means corridor friction scatter plots.
6. **Predictive Model Benchmark:** Error metric comparisons (RMSE, MAE, $R^2$) across candidate regressors.

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.10+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/<YOUR_GITHUB_USERNAME>/nassau-candy-optimization.git
cd nassau-candy-optimization

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit web dashboard
streamlit run app.py
```

The application will launch automatically in your browser at `http://localhost:8501`.

---

## 📂 Repository Structure

```
nassau-candy-optimization/
├── app.py                                # Streamlit production web application
├── train_models.py                       # ML pipeline: preprocessing, training & benchmarking
├── simulation_engine.py                  # Counterfactual simulator & multi-objective ranking
├── clustering_engine.py                  # K-Means route clustering & bottleneck lane detection
├── geodata.py                            # Coordinates, Haversine formula, spatial lookups
├── nassau_candy_orders.csv               # Historical shipment dataset (10,194 records)
├── nassau_candy_enriched.csv             # Enriched dataset with spatial and financial features
├── requirements.txt                      # Project dependencies for deployment
├── .streamlit/
│   └── config.toml                       # Theme, colors, and server configuration
├── models/                               # Saved model artifacts (.joblib, .json, .csv)
│   ├── best_model.joblib
│   ├── linear_regression.joblib
│   ├── random_forest.joblib
│   ├── gradient_boosting.joblib
│   ├── model_metrics.json
│   ├── route_clusters.csv
│   └── simulation_results.csv
├── research_paper/
│   ├── RESEARCH_PAPER.md                 # Full academic research paper (publication-ready)
│   └── EXECUTIVE_SUMMARY.md              # Policy brief for C-suite & government stakeholders
└── submission_guide/
    ├── PROJECT_FEEDBACK_VIDEO_SCRIPT.md  # Complete word-for-word recording script & checklist
    └── SUBMISSION_INSTRUCTIONS.md        # Step-by-step submission guide for the 4 portal fields
```

---

## 👥 Contributors & Acknowledgments

- **Lead Analyst:** Machine Learning & Logistics Data Science Team
- **Program:** Capstone Project with [Unified Mentor](https://www.unifiedmentor.com/)
- **Industry Partner:** [Nassau Candy Distributor](https://www.nassaucandy.com/)

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
