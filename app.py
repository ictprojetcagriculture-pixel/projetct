import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgriEconomics: Crop Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM THEMING / STYLE INJECTION ---
st.markdown("""
    <style>
    .main { background-color: #f9fbf9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #2e5a1c; }
    </style>
""", unsafe_allow_html=True)

# --- MOCK DATASTORE ---
# Rates and inputs optimized for Punjab/Pakistan regional averages and global markets.
# Values are normalized per ACRE. (1 Hectare = 2.47105 Acres)
CROP_DATA = {
    "Wheat (Gandum)": {
        "seed_req_kg_per_acre": 50,
        "seed_cost_per_kg": 120,
        "fertilizer_desc": "Urea: 2 bags/acre, DAP: 1 bag/acre",
        "pesticide_desc": "Sulfosulfuron for weed control, Rust prevention fungicides if humid.",
        "input_chemical_cost_per_acre": 18000,
        "labor_overhead_per_acre": 12000,
        "days_to_harvest": 140,
        "yield_tons_per_acre": 1.6,
        "local_rate_pkr_per_ton": 100000,       # ~4000 PKR per 40kg
        "export_rate_pkr_per_ton": 135000       # Global equivalent in PKR
    },
    "Rice (Basmati)": {
        "seed_req_kg_per_acre": 6,
        "seed_cost_per_kg": 450,
        "fertilizer_desc": "DAP: 1 bag/acre, Urea: 2 bags/acre, Zinc Sulfate: 10kg/acre",
        "pesticide_desc": "Pre-emergence herbicides (Butachlor), Cartap for stem borer control.",
        "input_chemical_cost_per_acre": 25000,
        "labor_overhead_per_acre": 20000,
        "days_to_harvest": 120,
        "yield_tons_per_acre": 1.8,
        "local_rate_pkr_per_ton": 225000,      # High value Basmati variety
        "export_rate_pkr_per_ton": 320000
    },
    "Cotton (Kapas)": {
        "seed_req_kg_per_acre": 8,
        "seed_cost_per_kg": 800,
        "fertilizer_desc": "DAP: 1.5 bags/acre, Urea: 3 bags/acre (split applications)",
        "pesticide_desc": "Targeted sprays for Whitefly, Pink Bollworm, and Jassids.",
        "input_chemical_cost_per_acre": 32000,
        "labor_overhead_per_acre": 22000,
        "days_to_harvest": 180,
        "yield_tons_per_acre": 1.0,
        "local_rate_pkr_per_ton": 210000,      # ~8400 PKR per 40kg
        "export_rate_pkr_per_ton": 260000
    },
    "Sugarcane (Kamad)": {
        "seed_req_kg_per_acre": 3000, # Uses seed sets/canes
        "seed_cost_per_kg": 12,
        "fertilizer_desc": "DAP: 2 bags/acre, Urea: 4-5 bags/acre, Potash: 1 bag/acre",
        "pesticide_desc": "Granular insecticides for Borers, Termite control chemical treatment.",
        "input_chemical_cost_per_acre": 40000,
        "labor_overhead_per_acre": 35000,
        "days_to_harvest": 300,
        "yield_tons_per_acre": 32.0,
        "local_rate_pkr_per_ton": 10000,        # ~400 PKR per 40kg
        "export_rate_pkr_per_ton": 13000
    },
    "Maize (Makai)": {
        "seed_req_kg_per_acre": 10,
        "seed_cost_per_kg": 1200, # Hybrid seeds
        "fertilizer_desc": "DAP: 2 bags/acre, Urea: 3 bags/acre, Zinc application",
        "pesticide_desc": "Fall Armyworm monitoring and emamectin benzoate application.",
        "input_chemical_cost_per_acre": 28000,
        "labor_overhead_per_acre": 15000,
        "days_to_harvest": 110,
        "yield_tons_per_acre": 3.5,
        "local_rate_pkr_per_ton": 70000,
        "export_rate_pkr_per_ton": 85000
    },
    "Potato (Aloo)": {
        "seed_req_kg_per_acre": 1200,
        "seed_cost_per_kg": 60,
        "fertilizer_desc": "DAP: 3 bags/acre, Urea: 2 bags/acre, SOP (Potash): 2 bags/acre",
        "pesticide_desc": "Fungicides for Early/Late Blight (Mancozeb), Aphid controls.",
        "input_chemical_cost_per_acre": 45000,
        "labor_overhead_per_acre": 25000,
        "days_to_harvest": 100,
        "yield_tons_per_acre": 11.0,
        "local_rate_pkr_per_ton": 45000,
        "export_rate_pkr_per_ton": 65000
    }
}

# --- HEADER SECTION ---
st.title("🌾 AgriEconomics: Interactive Crop & Decision Dashboard")
st.markdown("""
    Welcome to the smart farming economic evaluation tool. This dashboard calculates resource requirements, 
    estimated yields, timelines, and accurate financial projections (Profit/Loss analyses) 
    comparing local and export market channels.
    
    *Adjust variables in the sidebar to dynamically simulate risk, overhead, and investment yields.*
""")
st.write("---")

# --- SIDEBAR / USER INPUTS ---
st.sidebar.header("🌱 Configuration Parameters")

selected_crop = st.sidebar.selectbox(
    "Select Target Crop:",
    options=list(CROP_DATA.keys()),
    help="Search and pick a major commercial or subsistence crop."
)

unit_type = st.sidebar.radio(
    "Land Area Unit:",
    options=["Acres", "Hectares"],
    horizontal=True
)

land_area = st.sidebar.number_input(
    f"Enter Total Land Area ({unit_type}):",
    min_value=0.1,
    max_value=10000.0,
    value=5.0,
    step=0.5
)

available_budget = st.sidebar.number_input(
    "Total Available Budget (PKR):",
    min_value=1000,
    max_value=100000000,
    value=500000,
    step=10000,
    format="%d"
)

# --- UNIT CONVERSION LOGIC ---
# Standardize input values to internal acre measurements
acres_calculated = land_area if unit_type == "Acres" else land_area * 2.47105
crop_stats = CROP_DATA[selected_crop]

# --- MAIN PAGE CALCULATIONS ---
# 1. Total Requirements Calculations
total_seed_kg = crop_stats["seed_req_kg_per_acre"] * acres_calculated
total_seed_cost = total_seed_kg * crop_stats["seed_cost_per_kg"]
total_chemical_cost = crop_stats["input_chemical_cost_per_acre"] * acres_calculated
total_labor_cost = crop_stats["labor_overhead_per_acre"] * acres_calculated
total_estimated_cost = total_seed_cost + total_chemical_cost + total_labor_cost

# 2. Yield & Timeline Calculations
total_yield_tons = crop_stats["yield_tons_per_acre"] * acres_calculated
harvest_days = crop_stats["days_to_harvest"]

# 3. Revenue & Profit/Loss Generation
revenue_local = total_yield_tons * crop_stats["local_rate_pkr_per_ton"]
revenue_export = total_yield_tons * crop_stats["export_rate_pkr_per_ton"]

profit_local = revenue_local - total_estimated_cost
profit_export = revenue_export - total_estimated_cost

# --- DASHBOARD VISUALIZATIONS & OUTPUTS ---

# Row 1: Key Operational Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🌱 Total Seed Requirement", value=f"{total_seed_kg:,.1f} Kg")
with col2:
    st.metric(label="⚖️ Projected Total Yield", value=f"{total_yield_tons:,.2f} Tons")
with col3:
    st.metric(label="⏳ Time to Harvest", value=f"{harvest_days} Days (~{round(harvest_days/30, 1)} months)")

st.write("---")

# Row 2: Comprehensive Management Breakdown
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🛠️ Input & Treatment Specifications")
    st.markdown(f"**Recommended Fertilizer Treatment:**\n*{crop_stats['fertilizer_desc']}*")
    st.markdown(f"**Pesticide & Herbicide Controls:**\n*{crop_stats['pesticide_desc']}*")
    
    st.subheader("💰 Market Rates Comparison")
    rates_df = pd.DataFrame({
        "Market Type": ["Local Market (Punjab Base)", "International Export Rate"],
        "Rate per Ton (PKR)": [crop_stats["local_rate_pkr_per_ton"], crop_stats["export_rate_pkr_per_ton"]]
    })
    st.table(rates_df.set_index("Market Type"))

with right_col:
    st.subheader("📊 Financial Health Matrix")
    
    # Financial indicators
    st.write(f"**Total Cost of Production:** PKR {total_estimated_cost:,.2f}")
    
    # Budget Check Warning / Success
    if total_estimated_cost > available_budget:
        st.error(f"⚠️ **Budget Deficit:** Total costs exceed your available capital by PKR {total_estimated_cost - available_budget:,.2f}. Consider lowering cultivation acreage or securing financing.")
    else:
        st.success(f"✅ **Budget Safe:** Your capital is sufficient! You have a remaining reserve buffer of PKR {available_budget - total_estimated_cost:,.2f}.")
        
    # Profit presentation
    local_color = "green" if profit_local >= 0 else "red"
    export_color = "green" if profit_export >= 0 else "red"
    
    st.markdown(f"### Local Net Profit/Loss: <span style='color:{local_color}'>PKR {profit_local:,.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"### Export Net Profit/Loss: <span style='color:{export_color}'>PKR {profit_export:,.2f}</span>", unsafe_allow_html=True)

st.write("---")

# Row 3: Interactive Visual Risk/Reward Analysis Diagram
st.subheader("📉 Investment vs Return Cost Structure Breakdown")

# Setting up labels and data array for plotting
categories = ['Seed Costs', 'Chemicals/Fertilizers', 'Labor Overhead', 'Projected Net Local Profit', 'Projected Export Bonus']
costs_breakdown = [total_seed_cost, total_chemical_cost, total_labor_cost, max(0, profit_local), max(0, profit_export - profit_local if profit_export > profit_local else 0)]

fig = go.Figure(data=[
    go.Bar(
        x=categories,
        y=costs_breakdown,
        marker_color=['#d97706', '#059669', '#2563eb', '#16a34a', '#8b5cf6'],
        text=[f"PKR {val:,.0f}" for val in costs_breakdown],
        textposition='auto',
    )
])

fig.update_layout(
    title=f"Cost Distribution vs Yield Margins for {selected_crop} across {land_area} {unit_type}",
    xaxis_title="Financial Component",
    yaxis_title="Value (PKR)",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)
