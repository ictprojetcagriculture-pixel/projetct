import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="AgriGrow: Smart Agricultural Advisory Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 1. MOCK DATABASE SETUP
# -----------------------------------------------------------------------------
# Standardized crop data per acre
CROP_DB = {
    "Wheat": {
        "seeds_per_acre_kg": 50,
        "growth_days": 120,
        "pesticides": "Deltamethrin (0.5L/acre)",
        "herbicides": "Glyphosate (1.0L/acre)",
        "yield_per_acre_kg": 1600,
        "local_rate_per_kg": 100,       # e.g., PKR or local currency unit
        "intl_rate_per_kg": 140,
        "base_cost_per_acre": 45000     # Labor, water, tractor, fertilizer
    },
    "Rice": {
        "seeds_per_acre_kg": 8,
        "growth_days": 105,
        "pesticides": "Cartap Hydrochloride (1.2L/acre)",
        "herbicides": "Butachlor (0.8L/acre)",
        "yield_per_acre_kg": 2400,
        "local_rate_per_kg": 120,
        "intl_rate_per_kg": 180,
        "base_cost_per_acre": 65000
    },
    "Corn (Maize)": {
        "seeds_per_acre_kg": 10,
        "growth_days": 115,
        "pesticides": "Lambda-Cyhalothrin (0.4L/acre)",
        "herbicides": "Atrazine (1.5L/acre)",
        "yield_per_acre_kg": 3200,
        "local_rate_per_kg": 85,
        "intl_rate_per_kg": 110,
        "base_cost_per_acre": 55000
    },
    "Cotton": {
        "seeds_per_acre_kg": 6,
        "growth_days": 180,
        "pesticides": "Imidacloprid (0.6L/acre)",
        "herbicides": "Pendimethalin (1.2L/acre)",
        "yield_per_acre_kg": 1000,
        "local_rate_per_kg": 220,
        "intl_rate_per_kg": 280,
        "base_cost_per_acre": 70000
    }
}

# -----------------------------------------------------------------------------
# MAIN APP INTERFACE
# -----------------------------------------------------------------------------
st.title("🌾 AgriGrow Dashboard")
st.subheader("Interactive Agricultural Advisory & Financial Projection System")
st.markdown("---")

# -----------------------------------------------------------------------------
# SIDEBAR: STEP 1 & STEP 2 (USER INPUTS)
# -----------------------------------------------------------------------------
st.sidebar.header("📋 Input Configuration")

# Step 1: Crop Selection
selected_crop = st.sidebar.selectbox(
    "Step 1: Select Crop Type",
    options=list(CROP_DB.keys())
)

st.sidebar.markdown("---")

# Step 2: User Resources Input
st.sidebar.header("🚜 Land & Budget Resources")
land_acres = st.sidebar.number_input(
    "Available Land (in Acres)", 
    min_value=0.0, 
    value=1.0, 
    step=0.5,
    help="Enter total cultivable area in acres."
)

budget = st.sidebar.number_input(
    "Available Budget (Local Currency)", 
    min_value=0.0, 
    value=100000.0, 
    step=5000.0,
    help="Enter total capital allocated for this production cycle."
)

# -----------------------------------------------------------------------------
# BUSINESS LOGIC & PROCESSING
# -----------------------------------------------------------------------------
# Input Validation Check
if land_acres <= 0:
    st.error("⚠️ Error: Land area must be greater than 0 acres to generate projections.")
else:
    # Fetch active crop attributes
    crop_data = CROP_DB[selected_crop]
    
    total_seeds = crop_data["seeds_per_acre_kg"] * land_acres
    total_days = crop_data["growth_days"]
    total_yield = crop_data["yield_per_acre_kg"] * land_acres
    
    # Financial Calculations
    total_production_cost = crop_data["base_cost_per_acre"] * land_acres
    
    # Revenue calculations
    revenue_local = total_yield * crop_data["local_rate_per_kg"]
    revenue_intl = total_yield * crop_data["intl_rate_per_kg"]
    
    # Profit/Loss calculations
    profit_local = revenue_local - total_production_cost
    profit_loss_intl = revenue_intl - total_production_cost
    
    # Budget evaluation
    is_budget_sufficient = budget >= total_production_cost

    # -----------------------------------------------------------------------------
    # MAIN PANEL DISPLAY
    # -----------------------------------------------------------------------------
    
    # 🌟 STEP 3: RESOURCE ADVISORY
    st.header("🛡️ Step 3: Resource & Plant Protection Advisory")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Seeds Required", value=f"{total_seeds:,.1f} kg")
    with col2:
        st.metric(label="Estimated Growth Duration", value=f"{total_days} Days")
    with col3:
        st.metric(label="Expected Total Biomass Yield", value=f"{total_yield:,.1f} kg")

    st.subheader("🧪 Crop Protection Measures (Per Acre Formula Applied)")
    protection_df = pd.DataFrame({
        "Category": ["Pesticide Treatment", "Herbicide Control"],
        "Recommended Composition": [crop_data["pesticides"], crop_data["herbicides"]],
        "Total Scale Volume Needed": [
            f"{float(crop_data['pesticides'].split('(')[1].split('L')[0]) * land_acres:.2f} Liters",
            f"{float(crop_data['herbicides'].split('(')[1].split('L')[0]) * land_acres:.2f} Liters"
        ]
    })
    st.table(protection_df)
    
    st.markdown("---")

    # 🌟 STEP 4: FINANCIAL PROJECTIONS
    st.header("💰 Step 4: Cost Analysis & Profit/Loss Forecast")
    
    # Budget Warning Alert
    if not is_budget_sufficient:
        deficit = total_production_cost - budget
        st.error(f"⚠️ **Budget Alert:** Your available budget is insufficient. Estimated deficit is **{deficit:,.2f}** units.")
    else:
        st.success("✅ **Budget Validation:** Your available financial capital covers the estimated production costs.")

    col_cost, col_local, col_intl = st.columns(3)
    with col_cost:
        st.metric(
            label="Total Estimated Production Cost", 
            value=f"{total_production_cost:,.2f}",
            delta=f"Budget Match: {budget - total_production_cost:,.2f}" if is_budget_sufficient else f"-{total_production_cost - budget:,.2f}"
        )
        
    with col_local:
        st.metric(
            label="Projected Local Net Income", 
            value=f"{profit_local:,.2f}", 
            delta=f"Gross Rev: {revenue_local:,.2f}",
            delta_color="normal" if profit_local >= 0 else "inverse"
        )
        
    with col_intl:
        st.metric(
            label="Projected International Net Income", 
            value=f"{profit_loss_intl:,.2f}", 
            delta=f"Gross Rev: {revenue_intl:,.2f}",
            delta_color="normal" if profit_loss_intl >= 0 else "inverse"
        )

    # Reference Rates Sub-table
    st.subheader("📊 Current Market Trade Rates Reference")
    rates_df = pd.DataFrame({
        "Market Domain": ["Local Distribution Network", "International Trade Index"],
        "Rate Per KG": [f"{crop_data['local_rate_per_kg']:.2f}", f"{crop_data['intl_rate_per_kg']:.2f}"],
        "Gross Revenue Forecast": [f"{revenue_local:,.2f}", f"{revenue_intl:,.2f}"]
    })
    st.dataframe(rates_df, use_container_width=True)

    st.markdown("---")

    # 🌟 STEP 5: SMART ALTERNATIVE RECOMMENDATIONS
    st.header("💡 Step 5: Optimization & Smart Recommendations")
    
    # Logic condition for checking if alternatives are necessary
    if profit_local < 0 or not is_budget_sufficient:
        st.warning("⚠️ High Risk Detected: Current parameters project low profit margins or high capital tension.")
        st.write("### Recommended Alternatives:")
        
        viable_alternatives = []
        for crop, details in CROP_DB.items():
            if crop == selected_crop:
                continue
            
            alt_cost = details["base_cost_per_acre"] * land_acres
            alt_yield = details["yield_per_acre_kg"] * land_acres
            alt_profit_local = (alt_yield * details["local_rate_per_kg"]) - alt_cost
            
            if budget >= alt_cost and alt_profit_local > profit_local:
                viable_alternatives.append({
                    "Crop": crop,
                    "Production Cost": alt_cost,
                    "Expected Local Profit": alt_profit_local,
                    "Growth Cycle": f"{details['growth_days']} days"
                })
        
        if viable_alternatives:
            alt_df = pd.DataFrame(viable_alternatives)
            st.write("Switching to one of the following alternatives fits your profile constraints more efficiently:")
            st.dataframe(alt_df, use_container_width=True)
        else:
            st.info("No single alternative fits your exact constraint threshold perfectly. Consider reducing production land scale acreage down to lower input overhead requirements safely.")
    else:
        st.success("✨ Optimization Check: This operation exhibits solid operational safety profiles. Proceed with standard cultivation timeline patterns.")
