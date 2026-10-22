import os
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from geodata import (
    FACTORIES, PRODUCT_FACTORY_MAP, PRODUCT_DIVISION_MAP,
    haversine_distance, get_factory_coords
)
from simulation_engine import simulate_product_factory_assignments, generate_recommendations, compute_system_kpis

st.set_page_config(
    page_title="Nassau Candy - Factory Reallocation & Shipping Optimization",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #F59E0B;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #CBD5E1;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .risk-badge-low {
        background-color: #065F46;
        color: #A7F3D0;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .risk-badge-med {
        background-color: #92400E;
        color: #FDE68A;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .risk-badge-high {
        background-color: #991B1B;
        color: #FECACA;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if os.path.exists("nassau_candy_enriched.csv"):
        df = pd.read_csv("nassau_candy_enriched.csv")
    else:
        df = pd.read_csv("nassau_candy_orders.csv")
        df['Origin Factory'] = df['Product Name'].map(PRODUCT_FACTORY_MAP)
        df['Division'] = df['Product Name'].map(PRODUCT_DIVISION_MAP)
    return df

@st.cache_data
def load_metrics():
    metrics_path = "models/model_metrics.json"
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            return json.load(f)
    return {}

df_raw = load_data()
model_metrics = load_metrics()

# ================= SIDEBAR CONTROLS =================
st.sidebar.image("https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?auto=format&fit=crop&w=400&q=80", use_container_width=True)
st.sidebar.title("🎛️ Optimization Controls")

# Product selector
all_products = sorted(df_raw['Product Name'].unique().tolist())
selected_product = st.sidebar.selectbox("Select Product Focus", ["All Products"] + all_products)

# Region filter
all_regions = sorted(df_raw['Region'].unique().tolist())
selected_region = st.sidebar.multiselect("Destination Regions", all_regions, default=all_regions)

# Ship mode filter
all_modes = sorted(df_raw['Ship Mode'].unique().tolist())
selected_ship_modes = st.sidebar.multiselect("Ship Modes", all_modes, default=all_modes)

# Optimization Priority Slider (Speed vs Profit)
st.sidebar.markdown("---")
st.sidebar.subheader("⚖️ Objective Trade-Off")
speed_priority = st.sidebar.slider(
    "Optimization Priority",
    min_value=0.0,
    max_value=1.0,
    value=0.55,
    step=0.05,
    help="0.0 = Prioritize Profit & Low Reallocation Expense | 1.0 = Prioritize Maximum Speed & Minimum Lead Time"
)
st.sidebar.caption(f"Speed Weight: **{speed_priority*100:.0f}%** | Profit Weight: **{(1-speed_priority)*100:.0f}%**")

# Top-N recommendation count
top_n = st.sidebar.slider("Top Recommendations to Display", min_value=1, max_value=10, value=5)

# Filter dataset
filtered_df = df_raw.copy()
if selected_product != "All Products":
    filtered_df = filtered_df[filtered_df['Product Name'] == selected_product]
if selected_region:
    filtered_df = filtered_df[filtered_df['Region'].isin(selected_region)]
if selected_ship_modes:
    filtered_df = filtered_df[filtered_df['Ship Mode'].isin(selected_ship_modes)]

# Run or retrieve simulations
sim_df = simulate_product_factory_assignments(df_raw, speed_weight=speed_priority)
recs_df = generate_recommendations(sim_df, top_n=top_n)
kpis = compute_system_kpis(sim_df, recs_df)

# ================= MAIN HEADER =================
st.markdown('<div class="main-header">🏭 Factory Reallocation & Shipping Optimization</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Decision Intelligence Platform for Nassau Candy Distributor • Balancing Transit Lead Time, Operational Risk & Profitability</div>', unsafe_allow_html=True)

# ================= TOP KPI SCORECARD =================
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
with kpi_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Lead Time Reduction</div>
        <div class="metric-value">-{kpis['avg_lead_time_reduction_pct']}%</div>
        <div style="font-size:0.75rem; color:#10B981;">Operational Gain</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Profit Stability</div>
        <div class="metric-value">{kpis['profit_impact_stability']}%</div>
        <div style="font-size:0.75rem; color:#10B981;">Financial Safety</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Scenario Confidence</div>
        <div class="metric-value">{kpis['scenario_confidence_score']}%</div>
        <div style="font-size:0.75rem; color:#38BDF8;">Model Reliability</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Recommendation Coverage</div>
        <div class="metric-value">{kpis['recommendation_coverage']}%</div>
        <div style="font-size:0.75rem; color:#A78BFA;">Catalog Scalability</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Est. Freight Savings</div>
        <div class="metric-value">${kpis['total_annual_freight_savings']:,.2f}</div>
        <div style="font-size:0.75rem; color:#F59E0B;">Direct Cost Reduction</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ================= TABS NAVIGATION =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Optimization Simulator",
    "🔮 What-If Scenario Analysis",
    "💡 Recommendation Dashboard",
    "⚠️ Risk & Impact Alerts",
    "🗺️ Network & Route Clustering",
    "📈 Predictive Model Benchmark"
])

# ----------------- TAB 1: FACTORY OPTIMIZATION SIMULATOR -----------------
with tab1:
    st.subheader("🎯 Product Factory Assignment Simulator")
    st.markdown("Select any product to simulate shipping performance across all 5 candidate production facilities.")
    
    sim_prod = st.selectbox("Choose Product to Simulate", all_products, index=0, key="sim_prod_select")
    prod_sim_data = sim_df[sim_df['Product Name'] == sim_prod].sort_values(by="Composite Score", ascending=False)
    
    curr_factory_name = prod_sim_data[prod_sim_data['Is Current']]['Current Factory'].iloc[0]
    best_factory_row = prod_sim_data.iloc[0]
    
    c1, c2 = st.columns([1, 1])
    with c1:
        fig_bar = px.bar(
            prod_sim_data,
            x='Candidate Factory',
            y='Predicted Lead Time (Days)',
            color='Candidate Factory',
            text='Predicted Lead Time (Days)',
            title=f"Predicted Shipping Lead Time for '{sim_prod}' Across Factories",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_bar.add_hline(
            y=prod_sim_data[prod_sim_data['Is Current']]['Current Avg Lead Time (Days)'].iloc[0],
            line_dash="dash",
            line_color="#EF4444",
            annotation_text="Current Baseline"
        )
        fig_bar.update_layout(template="plotly_dark", showlegend=False, height=380)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        fig_score = px.bar(
            prod_sim_data,
            x='Candidate Factory',
            y='Composite Score',
            color='Composite Score',
            text='Composite Score',
            color_continuous_scale="Viridis",
            title=f"Composite Optimization Score (Speed Weight: {speed_priority*100:.0f}%)"
        )
        fig_score.update_layout(template="plotly_dark", height=380)
        st.plotly_chart(fig_score, use_container_width=True)
        
    st.markdown("#### Detailed Factory Comparison Matrix")
    display_sim_cols = [
        'Candidate Factory', 'Is Current', 'Divisional Fit', 'Predicted Lead Time (Days)',
        'Lead Time Reduction (%)', 'Simulated Avg Distance (km)', 'Distance Reduction (%)',
        'Profit Delta ($)', 'Composite Score', 'Risk Tier'
    ]
    st.dataframe(
        prod_sim_data[display_sim_cols].style.format({
            'Predicted Lead Time (Days)': '{:.2f}',
            'Lead Time Reduction (%)': '{:+.2f}%',
            'Simulated Avg Distance (km)': '{:,.1f}',
            'Distance Reduction (%)': '{:+.2f}%',
            'Profit Delta ($)': '{:+.2f}',
            'Composite Score': '{:.1f}'
        }),
        use_container_width=True
    )

# ----------------- TAB 2: WHAT-IF SCENARIO ANALYSIS -----------------
with tab2:
    st.subheader("🔮 What-If Scenario Analysis: Current vs. Recommended Assignments")
    st.markdown("Compare system-wide metrics between current static assignments and AI-optimized factory reassignments.")
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        # Lead time delta comparison across recommended products
        if not recs_df.empty:
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                name='Current Lead Time (Days)',
                x=recs_df['Product Name'],
                y=recs_df['Current Lead Time (Days)'],
                marker_color='#94A3B8'
            ))
            fig_comp.add_trace(go.Bar(
                name='Optimized Lead Time (Days)',
                x=recs_df['Product Name'],
                y=recs_df['Recommended Lead Time (Days)'],
                marker_color='#10B981'
            ))
            fig_comp.update_layout(
                barmode='group',
                title="Lead Time Comparison (Current vs Recommended)",
                template="plotly_dark",
                height=400,
                xaxis_tickangle=-25
            )
            st.plotly_chart(fig_comp, use_container_width=True)
        else:
            st.info("Current configuration is already optimal at the specified priority threshold.")
            
    with col_w2:
        # Distance reduction breakdown
        if not recs_df.empty:
            fig_dist = px.bar(
                recs_df,
                x='Product Name',
                y='Distance Reduction (%)',
                color='Distance Reduction (%)',
                text='Distance Reduction (%)',
                color_continuous_scale="Tealgrn",
                title="Shipping Distance Reduction (%) by Reassigned Product"
            )
            fig_dist.update_layout(template="plotly_dark", height=400, xaxis_tickangle=-25)
            st.plotly_chart(fig_dist, use_container_width=True)
            
    # Interactive scenario customizer
    st.markdown("---")
    st.subheader("🛠️ Interactive Custom Reassignment Simulator")
    st.markdown("Test manual reassignments and observe real-time predicted system outcomes:")
    
    sc_col1, sc_col2, sc_col3 = st.columns(3)
    with sc_col1:
        custom_prod = st.selectbox("Select Product", all_products, key="custom_sc_prod")
    with sc_col2:
        custom_curr_fact = PRODUCT_FACTORY_MAP[custom_prod]
        st.text_input("Current Assigned Factory", value=custom_curr_fact, disabled=True)
    with sc_col3:
        custom_target_fact = st.selectbox("Simulate Move To:", list(FACTORIES.keys()), key="custom_target")
        
    custom_row = sim_df[(sim_df['Product Name'] == custom_prod) & (sim_df['Candidate Factory'] == custom_target_fact)].iloc[0]
    
    sc_res1, sc_res2, sc_res3, sc_res4 = st.columns(4)
    sc_res1.metric("Predicted Lead Time", f"{custom_row['Predicted Lead Time (Days)']:.2f} Days", delta=f"{custom_row['Lead Time Delta (Days)']:.2f} Days", delta_color="inverse")
    sc_res2.metric("Distance Reduction", f"{custom_row['Distance Reduction (%)']:.1f}%")
    sc_res3.metric("Profit Impact", f"${custom_row['Profit Delta ($)']:+,.2f}")
    sc_res4.metric("Risk Assessment", custom_row['Risk Tier'])

# ----------------- TAB 3: RECOMMENDATION DASHBOARD -----------------
with tab3:
    st.subheader("💡 Top Reallocation Recommendations")
    st.markdown("Algorithmic recommendations ranked by efficiency gains, facility suitability, and gross margin safety.")
    
    if not recs_df.empty:
        st.dataframe(
            recs_df.style.format({
                'Current Lead Time (Days)': '{:.2f}',
                'Recommended Lead Time (Days)': '{:.2f}',
                'Lead Time Improvement (%)': '+{:.2f}%',
                'Distance Reduction (%)': '{:+.2f}%',
                'Est. Profit Gain ($)': '${:+,.2f}',
                'Composite Score': '{:.1f}',
                'Confidence Score (%)': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        # Download button for recommendations
        csv_recs = recs_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Recommendations to CSV",
            data=csv_recs,
            file_name="nassau_candy_recommendations.csv",
            mime="text/csv"
        )
    else:
        st.warning("No reallocations surpass the efficiency improvement threshold with the current weightings.")

# ----------------- TAB 4: RISK & IMPACT ALERTS -----------------
with tab4:
    st.subheader("⚠️ Risk & Operational Impact Panel")
    st.markdown("Comprehensive risk auditing to prevent disruption, margin erosion, and tooling mismatch.")
    
    r_col1, r_col2 = st.columns([1, 1])
    with r_col1:
        st.markdown("#### High-Risk Reassignment Warnings")
        high_risk_sims = sim_df[sim_df['Risk Tier'].str.contains("High", na=False)]
        
        st.error(f"⚠️ {len(high_risk_sims)} Factory-Product combinations flagged with High Risk.")
        st.markdown("""
        - **Facility Tooling Mismatch**: Assigning Chocolate lines to non-chocolate factories requires specialized conching and temperature-controlled tempering lines.
        - **Lead Time Degradation Warning**: Reassigning Pacific-centric products to Atlantic-border factories spikes standard shipping transit by up to 2.4 days.
        """)
        
        # Show sample high risk records
        st.dataframe(
            high_risk_sims[['Product Name', 'Candidate Factory', 'Risk Tier', 'Lead Time Reduction (%)', 'Profit Delta ($)']].head(6),
            use_container_width=True
        )
        
    with r_col2:
        st.markdown("#### Financial Margin Sensitivity Analysis")
        # Scatter of Profit impact vs Lead Time reduction
        fig_scatter = px.scatter(
            sim_df,
            x='Lead Time Reduction (%)',
            y='Profit Delta ($)',
            color='Risk Tier',
            hover_data=['Product Name', 'Candidate Factory'],
            title="Trade-Off Frontier: Profit Delta vs Lead Time Reduction",
            color_discrete_map={
                "Low (Recommended Efficiency Gain)": "#10B981",
                "Baseline (Current State)": "#60A5FA",
                "Medium (Margin Contraction)": "#F59E0B",
                "High (Lead Time Degradation)": "#EF4444",
                "High (Facility Re-tooling Required)": "#DC2626"
            }
        )
        fig_scatter.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------- TAB 5: NETWORK & ROUTE CLUSTERING -----------------
with tab5:
    st.subheader("🗺️ Supply Chain Network & Geographic Flow")
    
    # Map of factories and customer distribution centroids
    factory_map_data = []
    for f_name, f_info in FACTORIES.items():
        factory_map_data.append({
            'Name': f_name,
            'Lat': f_info['lat'],
            'Lon': f_info['lon'],
            'Type': 'Factory Origin',
            'City': f_info['city'],
            'State': f_info['state']
        })
    fact_map_df = pd.DataFrame(factory_map_data)
    
    fig_map = px.scatter_geo(
        fact_map_df,
        lat='Lat',
        lon='Lon',
        hover_name='Name',
        text='Name',
        title="Nassau Candy Manufacturing Facilities Coordinates",
        scope='usa'
    )
    fig_map.update_traces(marker=dict(size=14, color='#EF4444', symbol='diamond'))
    fig_map.update_layout(template="plotly_dark", height=420)
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔍 K-Means Route Performance Clustering")
    st.markdown("Unsupervised segmentation of shipping lanes by volume, distance, lead time, and profit margin.")
    
    if os.path.exists("models/route_clusters.csv"):
        rc_df = pd.read_csv("models/route_clusters.csv")
        fig_cluster = px.scatter(
            rc_df,
            x='avg_distance_km',
            y='avg_lead_time',
            size='order_count',
            color='Cluster_Label',
            hover_data=['Origin Factory', 'Region', 'Ship Mode'],
            title="Route Clusters: Transit Distance vs. Operational Lead Time",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_cluster.update_layout(template="plotly_dark", height=420)
        st.plotly_chart(fig_cluster, use_container_width=True)
        
        st.markdown("#### Congested Region-Product Bottlenecks")
        if os.path.exists("models/product_region_friction.csv"):
            fric_df = pd.read_csv("models/product_region_friction.csv")
            st.dataframe(
                fric_df[['Product Name', 'Region', 'Origin Factory', 'orders', 'avg_lead_time', 'avg_distance_km', 'Congestion_Score']].head(8).style.format({
                    'avg_lead_time': '{:.2f} Days',
                    'avg_distance_km': '{:,.1f} km',
                    'Congestion_Score': '{:.1f}'
                }),
                use_container_width=True
            )

# ----------------- TAB 6: PREDICTIVE MODEL BENCHMARK -----------------
with tab6:
    st.subheader("📈 Machine Learning Model Benchmarking")
    st.markdown("Evaluation metrics comparing Linear Regression baseline, Random Forest, and Gradient Boosting Regressor.")
    
    if model_metrics and 'models' in model_metrics:
        m_list = []
        for m_name, vals in model_metrics['models'].items():
            m_list.append({
                'Model': m_name,
                'Test RMSE (Days)': vals['test_rmse'],
                'Test MAE (Days)': vals['test_mae'],
                'Test R² Score': vals['test_r2'],
                'Train R² Score': vals['train_r2']
            })
        bench_df = pd.DataFrame(m_list)
        
        m_col1, m_col2 = st.columns([1, 1])
        with m_col1:
            st.dataframe(
                bench_df.style.format({
                    'Test RMSE (Days)': '{:.4f}',
                    'Test MAE (Days)': '{:.4f}',
                    'Test R² Score': '{:.4f}',
                    'Train R² Score': '{:.4f}'
                }).highlight_min(subset=['Test RMSE (Days)', 'Test MAE (Days)'], color='#065F46')
                  .highlight_max(subset=['Test R² Score'], color='#065F46'),
                use_container_width=True
            )
            st.success(f"🏆 Selected Champion Model: **{model_metrics.get('best_model', 'Linear Regression')}** based on lowest out-of-sample RMSE and high generalization stability.")
            
        with m_col2:
            fig_bench = px.bar(
                bench_df,
                x='Model',
                y=['Test RMSE (Days)', 'Test MAE (Days)'],
                barmode='group',
                title="Error Metric Benchmark (Lower is Better)",
                color_discrete_sequence=['#F59E0B', '#38BDF8']
            )
            fig_bench.update_layout(template="plotly_dark", height=320)
            st.plotly_chart(fig_bench, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>Nassau Candy Supply Chain Decision Intelligence System • Built for Unified Mentor & Nassau Candy Logistics Analytics</div>", unsafe_allow_html=True)
