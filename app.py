import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import math

# ==========================================
# 1. PAGE CONFIGURATION & STARTUP THEME
# ==========================================
st.set_page_config(
    page_title="AgriDrone OS",
    page_icon="🛸",
    layout="wide"
)

# Custom Startup CSS Injection
st.markdown("""
    <style>
    .metric-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #2E7D32;
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        color: #1B5E20;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. INTERNAL DATABASE & DATA SIMULATION
# ==========================================
@st.cache_data
def load_historical_data():
    """Generates an embedded historical log for analytics and model training."""
    np.random.seed(42)
    records = 150
    crops = ["Wheat", "Rice", "Cotton", "Maize", "Sugarcane"]
    
    data = {
        "farm_name": [f"Sector Alpha-{i}" for i in range(records)],
        "crop_type": np.random.choice(crops, records),
        "field_area": np.random.uniform(5, 120, records).round(2),
        "water_usage": np.random.uniform(100, 800, records).round(2),
        "fertilizer_usage": np.random.uniform(20, 150, records).round(2),
        "temperature": np.random.uniform(22, 40, records).round(1),
        "operational_cost": np.random.uniform(80, 500, records).round(2),
        "yield_tons": np.random.uniform(1.8, 7.5, records).round(2)
    }
    return pd.DataFrame(data)

hist_df = load_historical_data()

# Initialize Session Memory Store
if "current_farm" not in st.session_state:
    st.session_state.current_farm = {
        "farm_name": "Green Valley Base",
        "crop_type": "Wheat",
        "field_area": 25.0,
        "growth_stage": "Vegetative",
        "soil_moisture": 45.0,
        "infestation_level": "Low"
    }

# ==========================================
# 3. EMBEDDED MACHINE LEARNING CORE
# ==========================================
@st.cache_resource
def train_prediction_models(df):
    """Trains live Random Forest estimators right at runtime."""
    df_encoded = df.copy()
    le_crop = LabelEncoder()
    df_encoded['crop_encoded'] = le_crop.fit_transform(df_encoded['crop_type'])
    
    # Features for Yield and Cost
    X_yield = df_encoded[['field_area', 'crop_encoded', 'water_usage', 'fertilizer_usage', 'temperature']]
    y_yield = df_encoded['yield_tons']
    
    X_cost = df_encoded[['field_area', 'crop_encoded', 'fertilizer_usage', 'water_usage']]
    y_cost = df_encoded['operational_cost']
    
    model_yield = RandomForestRegressor(n_estimators=50, random_state=42).fit(X_yield, y_yield)
    model_cost = RandomForestRegressor(n_estimators=50, random_state=42).fit(X_cost, y_cost)
    
    return model_yield, model_cost, le_crop

yield_model, cost_model, encoder_crop = train_prediction_models(hist_df)

# ==========================================
# 4. SIDEBAR MANAGEMENT CONTROL
# ==========================================
st.sidebar.title("🌱 Farm Field Configuration")
st.sidebar.markdown("Update your operational workspace constraints below:")

with st.sidebar.form("global_farm_form"):
    sb_name = st.text_input("Farm Sector Identifier", value=st.session_state.current_farm["farm_name"])
    sb_crop = st.selectbox("Current Crop Rotation", ["Wheat", "Rice", "Cotton", "Maize", "Sugarcane"])
    sb_area = st.number_input("Total Field Area (Acres)", min_value=1.0, max_value=200.0, value=st.session_state.current_farm["field_area"])
    sb_stage = st.selectbox("Crop Growth Stage", ["Vegetative", "Flowering", "Ripening"])
    sb_moisture = st.slider("Measured Soil Moisture (%)", 0, 100, int(st.session_state.current_farm["soil_moisture"]))
    sb_infestation = st.select_slider("Observed Infestation Risk", options=["None", "Low", "Medium", "High"])
    
    if st.sidebar.form_submit_button("Sync Changes Globally"):
        st.session_state.current_farm = {
            "farm_name": sb_name, "crop_type": sb_crop, "field_area": sb_area,
            "growth_stage": sb_stage, "soil_moisture": sb_moisture, "infestation_level": sb_infestation
        }
        st.success("Telemetry Synced!")

# Read data effortlessly out of current state memory
farm = st.session_state.current_farm

# ==========================================
# 5. USER INTERFACE TABS CONTROL NAVIGATION
# ==========================================
st.title("🛸 Drone Spraying & Resource Optimizer")
st.markdown(f"**Active Workspace Engine:** Sector `{farm['farm_name']}` | Target Canopy Type: `{farm['crop_type']}`")

tab_dash, tab_flight, tab_weather, tab_health, tab_ml = st.tabs([
    "📊 Hub Dashboard", 
    "🛸 Flight Path Optimizer", 
    "🌤️ Environmental Intelligence", 
    "🌱 Canopy Health Analyzer", 
    "📈 Predictive ML Models"
])

# ------------------------------------------
# TAB 1: CONTROL HUB DASHBOARD
# ------------------------------------------
with tab_dash:
    st.subheader("Real-Time Asset Matrix Telemetry")
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"<div class='metric-card'><b>Monitored Sector</b><h3>{farm['farm_name']}</h3></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='metric-card'><b>Target Crop</b><h3>{farm['crop_type']}</h3></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='metric-card'><b>Assigned Scale</b><h3>{farm['field_area']} Acres</h3></div>", unsafe_allow_html=True)
    with k4:
        st.markdown(f"<div class='metric-card'><b>Growth Stage</b><h3>{farm['growth_stage']}</h3></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("**Real-Time Volumetric Soil Moisture Saturation Status:**")
    st.progress(int(farm["soil_moisture"]))
    
    st.markdown("---")
    st.subheader("Historical Analytics Profile Distributions")
    fig_hist = px.histogram(hist_df, x="field_area", color="crop_type", title="Regional Farm Land Scale Comparisons", 
                            color_discrete_sequence=px.colors.sequential.Darkmint, barmode="overlay")
    st.plotly_chart(fig_hist, use_container_width=True)

# ------------------------------------------
# TAB 2: FLIGHT PATH OPTIMIZER & MAPS
# ------------------------------------------
with tab_flight:
    st.subheader("Precision Navigation Logistics Configuration")
    
    c_p, c_r = st.columns([1, 2])
    
    with c_p:
        spray_mode = st.selectbox("Target Delivery Vector", ["Pesticide", "Fertilizer", "Water"])
        tank_cap = st.slider("UAV Payload Fluid Capacity (Liters)", 10, 50, 16)
        flight_speed = st.slider("Target Trajectory Speed (m/s)", 3, 15, 8)
        bat_cap = st.slider("Battery Cell Pack Rating (Ah)", 10, 30, 16)
        
        # Flight physics solver engine
        spray_configs = {"Pesticide": 15, "Fertilizer": 25, "Water": 50}
        vol_per_acre = spray_configs.get(spray_mode, 30)
        total_vol = farm["field_area"] * vol_per_acre
        
        flight_dist_km = round((farm["field_area"] * 4046.86 / 5) / 1000, 2)
        flight_time_min = round((flight_dist_km * 1000 / flight_speed) / 60, 1)
        refills = max(0, math.ceil(total_vol / tank_cap) - 1)
        
    with c_r:
        st.markdown("**Calculated Mission Parameters Output:**")
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("Total Fluid Target", f"{total_vol} Liters")
        rc2.metric("Total Flight Trajectory", f"{flight_dist_km} KM")
        rc3.metric("Refill Breaks Required", f"{refills}")
        
        st.markdown("<br>**Estimated Efficiency Savings Percentage (vs Traditional Flooding Systems):**")
        sc1, sc2 = st.columns(2)
        sc1.metric("Water Footprint Decrease", "72.4%", delta="Resource Reduction")
        sc2.metric("Time Asset Conservation", "84.1%", delta="Operational Optimization")

    st.markdown("---")
    st.subheader("Dynamic Flight Array Trajectory Mapping Canvas")
    
    lat, lon = 33.7743, 72.7521
    m = folium.Map(location=[lat, lon], zoom_start=15, tiles="OpenStreetMap")
    coords = [[lat-0.002, lon-0.002], [lat-0.002, lon+0.002], [lat+0.002, lon+0.002], [lat+0.002, lon-0.002]]
    folium.Polygon(locations=coords, color="#2E7D32", weight=3, fill=True, fill_opacity=0.1).add_to(m)
    for i in range(len(coords)-1):
        folium.PolyLine(locations=[coords[i], coords[i+1]], color="cyan", weight=2).add_to(m)
        
    st_folium(m, width=1100, height=350)

# ------------------------------------------
# TAB 3: ENVIRONMENTAL WEATHER INTELLIGENCE
# ------------------------------------------
with tab_weather:
    st.subheader("Atmospheric Risk Analysis Framework")
    
    wc1, wc2 = st.columns(2)
    with wc1:
        w_temp = st.slider("Ambient Heat Index (°C)", 15, 48, 31)
        w_wind = st.slider("Velocity Cross-Winds (km/h)", 0, 35, 12)
    with wc2:
        w_humid = st.slider("Relative Air Humidity (%)", 10, 100, 52)
        
    st.markdown("<br>**AI Flight Clearance Decision Output:**")
    if w_wind > 18:
        st.error("🚨 CRITICAL HAZARD: High velocity cross-winds will create excessive pesticide drift. Ground operations immediately.")
    elif w_temp > 38:
        st.warning("⚠️ EVAPORATION RISK: Temperatures exceed extreme spray thresholds. Droplets risk flash evaporation before canopy contact.")
    else:
        st.success("✅ OPTIMAL OPERATIONS: Environment meets clean tolerances. Proceed with scheduled autonomous flight maps.")

# ------------------------------------------
# TAB 4: CANOPY HEALTH SPECTRAL CORES
# ------------------------------------------
with tab_health:
    st.subheader("Simulated NDVI Spatial Biomass Distribution")
    
    # Generate spatial mock grid array data Matrix
    grid = np.random.rand(40, 40)
    if farm["infestation_level"] == "High": grid *= 0.35
    elif farm["infestation_level"] == "Medium": grid *= 0.65
    else: grid *= 0.92
    
    fig_map, ax = plt.subplots(figsize=(10, 3.5))
    cax = ax.imshow(grid, cmap="RdYlGn", origin="lower", vmin=0, vmax=1)
    fig_map.colorbar(cax, label="Calculated Biomass Vitality Scale")
    ax.axis('off')
    st.pyplot(fig_map)
    
    st.markdown(f"**Automated Diagnostic Assessment:** Cluster metrics tracking shows *{farm['infestation_level']}* localized canopy stress fields patterns.")

# ------------------------------------------
# TAB 5: PREDICTIVE MACHINE LEARNING CORE
# ------------------------------------------
with tab_ml:
    st.subheader("Advanced Inference Yield & Operational Overhead Engine")
    
    # Safely convert category types strings to match numerical fitted values arrays
    try:
        encoded_crop_val = encoder_crop.transform([farm["crop_type"]])[0]
    except:
        encoded_crop_val = 0
        
    mock_water = farm["field_area"] * 450.0 / 25.0
    mock_fertilizer = farm["field_area"] * 85.0 / 25.0
    
    # Run scikit-learn model object array vectors prediction
    input_vector_yield = np.array([[farm["field_area"], encoded_crop_val, mock_water, mock_fertilizer, 31.0]])
    input_vector_cost = np.array([[farm["field_area"], encoded_crop_val, mock_fertilizer, mock_water]])
    
    pred_yield = round(yield_model.predict(input_vector_yield)[0], 2)
    pred_cost = round(cost_model.predict(input_vector_cost)[0], 2)
    
    mc1, mc2 = st.columns(2)
    mc1.metric("ML Forecasted Seasonal Biomass Yield Output", f"{pred_yield} Tons")
    mc2.metric("ML Estimated Fleet Mechanical Maintenance Overhead", f"${pred_cost}")
    
    st.markdown("---")
    st.subheader("Export Center System Registry")
    csv_string = hist_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download System Log Telemetry History File (.CSV)", data=csv_string, file_name="agridrone_telemetry_report.csv", mime="text/csv")
