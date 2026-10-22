# Nassau Candy Distributor: Project Feedback Video Script & Recording Guide

This document provides a **complete, word-for-word script** and visual outline for recording your **Project Feedback Video** required for the Unified Mentor submission form.

> **Target Video Duration:** 3 to 5 minutes  
> **Format:** Screen recording with webcam (using Loom, OBS Studio, Zoom, or Google Meet).  
> **Recommended Hosting:** YouTube (Unlisted or Public) or Google Drive (Set link access to "Anyone with the link can view").

---

## Video Outline & Timestamp Guide

| Section | Timestamp | Key Focus |
| :--- | :---: | :--- |
| **1. Introduction** | 0:00 - 0:40 | Student Intro, Project Title, Unified Mentor Context |
| **2. Problem Statement** | 0:40 - 1:20 | Legacy static allocation, long shipping times, margin erosion |
| **3. Analytical Methodology & ML** | 1:20 - 2:30 | Data cleaning, Haversine formula, LR/RF/GBR benchmarking, clustering |
| **4. Live Dashboard Walkthrough** | 2:30 - 3:45 | Streamlit demo: Simulator, What-If analysis, recommendations, maps |
| **5. Business Insights & Learnings** | 3:45 - 4:30 | Sugar Shack reallocation, speed vs. profit trade-offs, technical takeaways |
| **6. Conclusion & Thank You** | 4:30 - 5:00 | Professional wrap-up and acknowledgment of Unified Mentor |

---

## Word-for-Word Speaking Script

### [0:00 - 0:40] Introduction
*"Hello everyone! My name is [Your Name], and today I am excited to present my capstone project with Unified Mentor: the **Factory Reallocation and Shipping Optimization Recommendation System for Nassau Candy Distributor**.*

*Nassau Candy is one of North America's leading confectionery distributors, supplying major retailers across fifty US states and Canada. As their customer demand has expanded, leadership was faced with a critical question: **What operational changes must we make to improve performance, reduce lead times, and preserve profitability?** Today, I will walk you through the end-to-end decision intelligence system I developed to answer that exact question."*

---

### [0:40 - 1:20] Problem Statement & Business Context
*(Show the Problem Statement slide or dataset preview)*

*"Historically, Nassau Candy assigned products to manufacturing plants using static rules and legacy habits. For example, all sugar candy was locked into a facility in northern Minnesota, while chocolates were split between Arizona and Georgia.*

*This static assignment created three major issues:*
1. *Suboptimal shipping distances, requiring cross-country trucking over thousands of kilometers.*
2. *Extended delivery lead times for retail stores in high-demand regions.*
3. *Margin erosion due to high freight expenses.*

*Prior to this project, leadership had no analytical tool to simulate factory reassignment scenarios, quantify operational impacts, or recommend optimal configurations at scale."*

---

### [1:20 - 2:30] Methodology, Machine Learning & Clustering
*(Show the Machine Learning Benchmark slide or Tab 6 on the dashboard)*

*"To build this decision intelligence platform, I followed a rigorous, step-by-step analytical methodology:*

*First, in **Data Preparation**, I enriched over 10,000 order records by engineering spatial features. Using the exact geographic coordinates of Nassau Candy's five factories and customer destinations, I calculated geodesic transit distances using the Haversine formula.*

*Next, for **Predictive Modeling**, I trained and evaluated three machine learning algorithms to predict shipping lead time:*
- *Linear Regression as our baseline,*
- *Random Forest Regressor, and*
- *Gradient Boosting Regressor.*

*Both the Linear Regression and Gradient Boosting models delivered outstanding accuracy with an $R^2$ of **0.9699** and a Root Mean Squared Error of just **0.24 days**, proving that our feature pipeline captured the operational dynamics of transit time.*

*In addition, I implemented **Unsupervised Route Clustering** using K-Means to categorize shipping corridors into high-efficiency lanes, core volume arteries, and severe cross-country bottleneck routes."*

---

### [2:30 - 3:45] Live Streamlit Application Walkthrough
*(Share your screen showing your running Streamlit Dashboard)*

*"Now, let me demonstrate the interactive Streamlit Web Application that operationalizes these models:*

*(Point to Top KPI Cards)*
*At the top, we see our executive scorecard: an estimated **3.3% to 8.5% lead time reduction**, **99.5% profit stability**, and an **80%+ scenario confidence score**.*

*(Click on Tab 1: Factory Optimization Simulator)*
*In the **Factory Optimization Simulator**, a logistics manager can select any product—for instance, SweeTARTS or Fun Dip—and immediately see predicted lead times and composite scores across all five manufacturing plants.*

*(Click on Tab 2: What-If Scenario Analysis & Move Priority Slider)*
*In the **What-If Scenario Analysis**, we can dynamically adjust the **Optimization Priority Slider**. If leadership prioritizes maximum delivery speed, the system balances lead time reduction; if leadership prioritizes profit, it guards against re-tooling capital expenses.*

*(Click on Tab 3: Recommendation Dashboard)*
*In the **Recommendation Dashboard**, the system outputs ranked, actionable reassignments. For example, it recommends moving high-volume sugar confections from the remote **Sugar Shack** in Minnesota to the centrally located **Secret Factory** in Illinois, cutting shipping distance by over 26%.*

*(Click on Tab 4 & 5: Risk Panel and Map)*
*Finally, the **Risk and Impact Panel** flags any facility tooling mismatches to protect chocolate production integrity, while the **Supply Chain Map** visualizes our manufacturing network across North America."*

---

### [3:45 - 4:30] Key Insights & Personal Learnings
*(Switch back to webcam or summary slide)*

*"This project provided immense learning opportunities:*
1. *First, I learned how to move from purely descriptive analytics to **prescriptive decision intelligence**—building systems that don't just explain what happened, but recommend what leadership should do next.*
2. *Second, I deepened my technical expertise in combining **spatial geometry, machine learning regression, and multi-objective optimization**.*
3. *Third, I gained a practical appreciation for balancing competing business trade-offs—such as logistics speed versus factory re-tooling risk.*

*The primary takeaway is clear: by relocating peripheral sugar products to central Midwest hubs, Nassau Candy can accelerate shipping, lower carbon emissions, and protect operating margins without risking chocolate line disruptions."*

---

### [4:30 - 5:00] Conclusion & Acknowledgments
*"In conclusion, this project provides Nassau Candy Distributor with a scalable, data-driven framework that transforms supply chain strategy from static legacy habits to intelligent optimization.*

*I want to express my sincere gratitude to the mentors and team at **Unified Mentor** for their guidance and for providing such an industry-relevant capstone challenge.*

*Thank you so much for watching, and I welcome any questions or feedback!"*

---

## Practical Recording Checklist

- [ ] **Lighting & Audio:** Ensure you are in a quiet room with good lighting and clear microphone audio.
- [ ] **Screen Resolution:** Run Streamlit at 100% browser zoom for crisp visibility.
- [ ] **Tabs Ready:** Have your Streamlit app running and opened in your browser before starting the recording.
- [ ] **Upload:** Upload the MP4 video to **YouTube** (set visibility to "Unlisted" so anyone with the link can view it) or **Google Drive** (ensure General Access is set to "Anyone with the link can view").
- [ ] **Test Link:** Paste the link in an incognito window to verify it opens smoothly without asking for a password.
