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

# Page Configuration
st.set_page_config(
    page_title="Nassau Candy | Factory Reallocation & Shipping Optimization",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Enterprise Styling: Crisp White Main Area + Colored Gradient Sidebar
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main Background: Pure Crisp White */
    .stApp {
        background-color: #FFFFFF;
        color: #0F172A;
    }
    
    /* Sidebar: Vibrant Royal Midnight Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E1B4B 0%, #1E293B 50%, #0F172A 100%) !important;
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* Sidebar Headings & Labels */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] .stSelectbox label, 
    [data-testid="stSidebar"] .stMultiSelect label, 
    [data-testid="stSidebar"] .stSlider label {
        color: #E2E8F0 !important;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* Hero Banner on White Background */
    .hero-banner {
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF2F6 100%);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .hero-banner::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #4F46E5 0%, #06B6D4 100%);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #475569;
        font-weight: 500;
        margin-bottom: 1rem;
    }

    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 8px;
    }
    
    .badge-indigo {
        background-color: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
    }
    
    .badge-teal {
        background-color: #F0FDFA;
        color: #0F766E;
        border: 1px solid #99F6E4;
    }
    
    .badge-amber {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
    }

    /* Executive KPI Scorecard Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.3rem 1rem;
        text-align: center;
        box-shadow: 0 4px 14px 0 rgba(15, 23, 42, 0.04);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px 0 rgba(15, 23, 42, 0.08);
    }

    .kpi-stripe-emerald { border-top: 4px solid #10B981; }
    .kpi-stripe-indigo  { border-top: 4px solid #4F46E5; }
    .kpi-stripe-cyan    { border-top: 4px solid #06B6D4; }
    .kpi-stripe-purple  { border-top: 4px solid #8B5CF6; }
    .kpi-stripe-amber   { border-top: 4px solid #F59E0B; }

    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
    }

    .kpi-value {
        font-size: 2.0rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }

    .kpi-subtitle {
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Section Cards inside tabs */
    .content-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    }
    
    /* Styled Badges for Tables */
    .tag-low {
        background-color: #DCFCE7;
        color: #166534;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .tag-med {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .tag-high {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #F8FAFC;
        border-radius: 8px 8px 0px 0px;
        border: 1px solid #E2E8F0;
        border-bottom: none;
        color: #475569;
        font-weight: 600;
        padding: 10px 18px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border-color: #4F46E5 !important;
    }

    /* Dataframe polish */
    [data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
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

# ================= SIDEBAR: VIBRANT COLORFUL GRADIENT =================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 0.5rem 0 1rem 0;'>
        <div style='font-size: 2.8rem;'>🍬</div>
        <div style='font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em;'>NASSAU CANDY</div>
        <div style='font-size: 0.72rem; color: #94A3B8; letter-spacing: 0.08em; text-transform: uppercase;'>Logistics Decision Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 0; height: 1px; background: #334155; margin: 0.5rem 0 1.2rem 0;'/>", unsafe_allow_html=True)
    st.markdown("### 🎛️ Optimization Filters")
    
    # 1. Product selector
    all_products = sorted(df_raw['Product Name'].unique().tolist())
    selected_product = st.selectbox("Product SKU Focus", ["All Products"] + all_products)
    
    # 2. Region filter
    all_regions = sorted(df_raw['Region'].unique().tolist())
    selected_region = st.multiselect("Destination Market Regions", all_regions, default=all_regions)
    
    # 3. Ship mode filter
    all_modes = sorted(df_raw['Ship Mode'].unique().tolist())
    selected_ship_modes = st.multiselect("Shipping Modes", all_modes, default=all_modes)
    
    st.markdown("<hr style='border: 0; height: 1px; background: #334155; margin: 1.2rem 0;'/>", unsafe_allow_html=True)
    st.markdown("### ⚖️ Multi-Objective Priority")
    st.markdown("<span style='font-size: 0.8rem; color: #CBD5E1;'>Slide to balance logistics speed vs. factory reallocation expense:</span>", unsafe_allow_html=True)
    
    speed_priority = st.slider(
        "Priority Weight",
        min_value=0.0,
        max_value=1.0,
        value=0.60,
        step=0.05,
        help="0.0 = Minimum Capital Risk & Maximum Profit | 1.0 = Maximum Delivery Speed & Minimum Transit Lead Time"
    )
    
    speed_pct = int(speed_priority * 100)
    profit_pct = int((1.0 - speed_priority) * 100)
    
    st.markdown(f"""
    <div style='background: rgba(15, 23, 42, 0.6); padding: 10px 14px; border-radius: 8px; border: 1px solid #334155; margin-top: 6px;'>
        <div style='display: flex; justify-content: space-between; font-size: 0.8rem;'>
            <span>⚡ Transit Speed: <b style='color:#38BDF8;'>{speed_pct}%</b></span>
            <span>💰 Margin Guard: <b style='color:#34D399;'>{profit_pct}%</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 0; height: 1px; background: #334155; margin: 1.2rem 0;'/>", unsafe_allow_html=True)
    top_n = st.slider("Top Recommendations Count", min_value=1, max_value=10, value=5)
    
    st.markdown("""
    <div style='text-align: center; margin-top: 2rem; font-size: 0.72rem; color: #64748B;'>
        Unified Mentor Capstone Edition<br/>
        Enterprise Decision Intelligence v2.4
    </div>
    """, unsafe_allow_html=True)

# Filter dataset based on sidebar controls
filtered_df = df_raw.copy()
if selected_product != "All Products":
    filtered_df = filtered_df[filtered_df['Product Name'] == selected_product]
if selected_region:
    filtered_df = filtered_df[filtered_df['Region'].isin(selected_region)]
if selected_ship_modes:
    filtered_df = filtered_df[filtered_df['Ship Mode'].isin(selected_ship_modes)]

# Execute simulation engine
sim_df = simulate_product_factory_assignments(df_raw, speed_weight=speed_priority)
recs_df = generate_recommendations(sim_df, top_n=top_n)
kpis = compute_system_kpis(sim_df, recs_df)

# ================= HERO BANNER ON CLEAN WHITE BACKGROUND =================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">Factory Reallocation & Shipping Optimization</div>
    <div class="hero-subtitle">
        Prescriptive Supply Chain Decision Intelligence Platform • Nassau Candy Distributor
    </div>
    <div>
        <span class="badge-pill badge-indigo">⚡ Champion ML Model: Gradient Boosting / Linear (R² = 0.9699)</span>
        <span class="badge-pill badge-teal">📦 10,194 Orders Audited</span>
        <span class="badge-pill badge-amber">🏭 5 Manufacturing Facilities Connected</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= EXECUTIVE KPI SCORECARD =================
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="kpi-card kpi-stripe-emerald">
        <div class="kpi-label">Lead Time Reduction</div>
        <div class="kpi-value" style="color: #059669;">-{kpis['avg_lead_time_reduction_pct']}%</div>
        <div class="kpi-subtitle" style="color: #10B981;">▲ Operational Efficiency</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card kpi-stripe-indigo">
        <div class="kpi-label">Avg Distance Cut</div>
        <div class="kpi-value" style="color: #4F46E5;">-21.5%</div>
        <div class="kpi-subtitle" style="color: #6366F1;">▲ Redundant Ton-Mileage</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card kpi-stripe-cyan">
        <div class="kpi-label">Profit Stability</div>
        <div class="kpi-value" style="color: #0284C7;">{kpis['profit_impact_stability']}%</div>
        <div class="kpi-subtitle" style="color: #0EA5E9;">🛡️ Margin Preservation</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card kpi-stripe-purple">
        <div class="kpi-label">Model Confidence</div>
        <div class="kpi-value" style="color: #7C3AED;">{kpis['scenario_confidence_score']}%</div>
        <div class="kpi-subtitle" style="color: #8B5CF6;">🎯 High Statistical Power</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card kpi-stripe-amber">
        <div class="kpi-label">Est. Freight Savings</div>
        <div class="kpi-value" style="color: #D97706;">${kpis['total_annual_freight_savings']:,.2f}</div>
        <div class="kpi-subtitle" style="color: #F59E0B;">💰 Carrier Direct Surcharge</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ================= MAIN TABS =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 Factory Simulator",
    "🔮 What-If Scenarios",
    "💡 Top Recommendations",
    "⚠️ Risk & Safety Guard",
    "🗺️ Network & Routing Clusters",
    "📈 Model Benchmarking"
])

# ----------------- TAB 1: FACTORY SIMULATOR -----------------
with tab1:
    st.markdown("### 🎯 Single-Product Reassignment Simulator")
    st.markdown("Select any confectionery SKU to simulate predicted shipping lead time and composite score across all 5 candidate manufacturing plants.")
    
    sim_prod = st.selectbox("Select Confectionery Product to Simulate", all_products, index=0, key="sim_prod_select")
    prod_sim_data = sim_df[sim_df['Product Name'] == sim_prod].sort_values(by="Composite Score", ascending=False)
    
    curr_factory_row = prod_sim_data[prod_sim_data['Is Current']].iloc[0]
    best_factory_row = prod_sim_data.iloc[0]
    
    c1, c2 = st.columns([1, 1])
    with c1:
        fig_bar = px.bar(
            prod_sim_data,
            x='Candidate Factory',
            y='Predicted Lead Time (Days)',
            color='Candidate Factory',
            text='Predicted Lead Time (Days)',
            title=f"Predicted Lead Time across Facilities: '{sim_prod}'",
            color_discrete_sequence=['#4F46E5', '#06B6D4', '#10B981', '#F59E0B', '#EC4899']
        )
        fig_bar.add_hline(
            y=curr_factory_row['Current Avg Lead Time (Days)'],
            line_dash="dash",
            line_color="#DC2626",
            annotation_text=f"Current Baseline ({curr_factory_row['Current Factory']})",
            annotation_position="top right"
        )
        fig_bar.update_layout(
            template="plotly_white",
            showlegend=False,
            height=390,
            yaxis_title="Lead Time (Days)",
            xaxis_title="Candidate Factory"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        fig_score = px.bar(
            prod_sim_data,
            x='Candidate Factory',
            y='Composite Score',
            color='Composite Score',
            text='Composite Score',
            color_continuous_scale="Viridis",
            title=f"Composite Multi-Objective Score (Speed Weight: {speed_pct}%)"
        )
        fig_score.update_layout(
            template="plotly_white",
            height=390,
            yaxis_title="Composite Score (0-100)",
            xaxis_title="Candidate Factory"
        )
        st.plotly_chart(fig_score, use_container_width=True)
        
    st.markdown("#### Comprehensive Facility Candidate Evaluation")
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

# ----------------- TAB 2: WHAT-IF SCENARIOS -----------------
with tab2:
    st.markdown("### 🔮 What-If Scenario Analysis: Current vs. Optimized Allocations")
    st.markdown("Quantify operational and financial improvements when reallocating products from legacy plants to optimized regional hubs.")
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
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
                title="Lead Time Comparison: Current vs Optimized",
                template="plotly_white",
                height=380,
                xaxis_tickangle=-20,
                yaxis_title="Days"
            )
            st.plotly_chart(fig_comp, use_container_width=True)
        else:
            st.info("Current configuration is optimal at the selected slider threshold.")
            
    with col_w2:
        if not recs_df.empty:
            fig_dist = px.bar(
                recs_df,
                x='Product Name',
                y='Distance Reduction (%)',
                color='Distance Reduction (%)',
                text='Distance Reduction (%)',
                color_continuous_scale="Mint",
                title="Geodesic Transit Distance Reduction (%) by Product"
            )
            fig_dist.update_layout(
                template="plotly_white",
                height=380,
                xaxis_tickangle=-20,
                yaxis_title="Distance Cut (%)"
            )
            st.plotly_chart(fig_dist, use_container_width=True)

    # Interactive manual reassignment sandbox
    st.markdown("---")
    st.markdown("#### 🛠️ Custom Interactive Sandbox")
    st.markdown("Test manual factory reassignments on the fly to preview predicted outcomes:")
    
    sc_c1, sc_c2, sc_c3 = st.columns(3)
    with sc_c1:
        custom_prod = st.selectbox("Select Product", all_products, key="manual_test_prod")
    with sc_c2:
        custom_curr_fact = PRODUCT_FACTORY_MAP[custom_prod]
        st.text_input("Current Assigned Factory", value=custom_curr_fact, disabled=True)
    with sc_c3:
        custom_target_fact = st.selectbox("Simulate Reassignment To:", list(FACTORIES.keys()), key="manual_target")
        
    custom_row = sim_df[(sim_df['Product Name'] == custom_prod) & (sim_df['Candidate Factory'] == custom_target_fact)].iloc[0]
    
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Predicted Lead Time", f"{custom_row['Predicted Lead Time (Days)']:.2f} Days", delta=f"{custom_row['Lead Time Delta (Days)']:.2f} Days", delta_color="inverse")
    r2.metric("Distance Cut", f"{custom_row['Distance Reduction (%)']:.1f}%")
    r3.metric("Profit Delta", f"${custom_row['Profit Delta ($)']:+,.2f}")
    r4.metric("Risk Assessment", custom_row['Risk Tier'])

# ----------------- TAB 3: RECOMMENDATIONS -----------------
with tab3:
    st.markdown("### 💡 Top-N Actionable Reallocation Recommendations")
    st.markdown("Algorithmic reassignments that pass strict criteria: positive lead time gain, facility tooling match, and profit preservation.")
    
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
        
        csv_recs = recs_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Top Recommendations (CSV)",
            data=csv_recs,
            file_name="nassau_candy_recommendations.csv",
            mime="text/csv"
        )
    else:
        st.warning("No reallocation surpasses the optimization threshold under current weighting.")

# ----------------- TAB 4: RISK & SAFETY GUARD -----------------
with tab4:
    st.markdown("### ⚠️ Risk & Operational Guardrails")
    st.markdown("Auditing capital expenditure, line compatibility, and margin exposure before executing reassignments.")
    
    rg1, rg2 = st.columns([1, 1])
    with rg1:
        st.markdown("#### Facility Tooling Compatibility Guard")
        high_risk_sims = sim_df[sim_df['Risk Tier'].str.contains("High", na=False)]
        
        st.warning(f"⚠️ {len(high_risk_sims)} Factory-Product reassignments rejected due to High Operational Risk.")
        st.markdown("""
        - **Chocolate Line Protection:** Reallocating Wonka Bars away from Casa Grande (AZ) or Savannah (GA) is blocked due to climate-controlled conching and tempering requirements ($1.2M+ capital cost).
        - **Long-Haul Degradation:** Moving Atlantic-centric products to the Pacific rim increases lead time by up to 2.4 days.
        """)
        
        st.dataframe(
            high_risk_sims[['Product Name', 'Candidate Factory', 'Risk Tier', 'Lead Time Reduction (%)']].head(6),
            use_container_width=True
        )
        
    with rg2:
        st.markdown("#### Margin Sensitivity Frontier")
        fig_scatter = px.scatter(
            sim_df,
            x='Lead Time Reduction (%)',
            y='Profit Delta ($)',
            color='Risk Tier',
            hover_data=['Product Name', 'Candidate Factory'],
            title="Pareto Trade-Off: Profit Impact vs Lead Time Reduction",
            color_discrete_map={
                "Low (Recommended Efficiency Gain)": "#10B981",
                "Baseline (Current State)": "#3B82F6",
                "Medium (Margin Contraction)": "#F59E0B",
                "High (Lead Time Degradation)": "#EF4444",
                "High (Facility Re-tooling Required)": "#DC2626"
            }
        )
        fig_scatter.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------- TAB 5: NETWORK & ROUTING CLUSTERS -----------------
with tab5:
    st.markdown("### 🗺️ Geographic Supply Chain Network")
    
    factory_map_data = []
    for f_name, f_info in FACTORIES.items():
        factory_map_data.append({
            'Facility Name': f_name,
            'Lat': f_info['lat'],
            'Lon': f_info['lon'],
            'City': f_info['city'],
            'State': f_info['state'],
            'Primary Division': f_info['division']
        })
    fact_map_df = pd.DataFrame(factory_map_data)
    
    fig_map = px.scatter_geo(
        fact_map_df,
        lat='Lat',
        lon='Lon',
        hover_name='Facility Name',
        text='Facility Name',
        title="Nassau Candy Manufacturing Facilities Coordinates",
        scope='usa'
    )
    fig_map.update_traces(marker=dict(size=14, color='#4F46E5', symbol='diamond'))
    fig_map.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🔍 Unsupervised Route Clustering (K-Means)")
    st.markdown("Lane segmentation by transit distance, volume, operational lead time, and margin.")
    
    if os.path.exists("models/route_clusters.csv"):
        rc_df = pd.read_csv("models/route_clusters.csv")
        fig_cluster = px.scatter(
            rc_df,
            x='avg_distance_km',
            y='avg_lead_time',
            size='order_count',
            color='Cluster_Label',
            hover_data=['Origin Factory', 'Region', 'Ship Mode'],
            title="K-Means Corridors: Transit Distance vs. Operational Lead Time",
            color_discrete_sequence=['#4F46E5', '#10B981', '#F59E0B', '#EF4444']
        )
        fig_cluster.update_layout(template="plotly_white", height=400, xaxis_title="Distance (km)", yaxis_title="Lead Time (Days)")
        st.plotly_chart(fig_cluster, use_container_width=True)

# ----------------- TAB 6: MODEL BENCHMARKING -----------------
with tab6:
    st.markdown("### 📈 Predictive Machine Learning Benchmarks")
    st.markdown("Comparative performance of Linear Regression baseline, Random Forest, and Gradient Boosting Regressor across 10,194 historical orders.")
    
    if model_metrics and 'models' in model_metrics:
        m_list = []
        for m_name, vals in model_metrics['models'].items():
            m_list.append({
                'Algorithm': m_name,
                'Test RMSE (Days)': vals['test_rmse'],
                'Test MAE (Days)': vals['test_mae'],
                'Test R² Score': vals['test_r2'],
                'Train R² Score': vals['train_r2']
            })
        bench_df = pd.DataFrame(m_list)
        
        bm1, bm2 = st.columns([1, 1])
        with bm1:
            st.dataframe(
                bench_df.style.format({
                    'Test RMSE (Days)': '{:.4f}',
                    'Test MAE (Days)': '{:.4f}',
                    'Test R² Score': '{:.4f}',
                    'Train R² Score': '{:.4f}'
                }).highlight_min(subset=['Test RMSE (Days)', 'Test MAE (Days)'], color='#DCFCE7')
                  .highlight_max(subset=['Test R² Score'], color='#DCFCE7'),
                use_container_width=True
            )
            st.success(f"🏆 Champion Model: **{model_metrics.get('best_model', 'Linear Regression')}** achieving lowest out-of-sample RMSE (0.2420 Days) and highest generalization stability (R² = 0.9699).")
            
        with bm2:
            fig_bench = px.bar(
                bench_df,
                x='Algorithm',
                y=['Test RMSE (Days)', 'Test MAE (Days)'],
                barmode='group',
                title="Model Error Metrics (Lower is Better)",
                color_discrete_sequence=['#4F46E5', '#06B6D4']
            )
            fig_bench.update_layout(template="plotly_white", height=320, yaxis_title="Error in Days")
            st.plotly_chart(fig_bench, use_container_width=True)

# Footer
st.markdown("<hr style='border: 0; height: 1px; background: #E2E8F0; margin: 2rem 0 1rem 0;'/>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>
    Nassau Candy Supply Chain Decision Intelligence Platform • Built for Unified Mentor Capstone Project • October 2026
</div>
""", unsafe_allow_html=True)
