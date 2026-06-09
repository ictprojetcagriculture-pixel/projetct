import streamlit as st
import plotly.express as px
import pandas as pd
from modules.database import save_farm_record

st.title("🌾 Command Dashboard & Farm Configurator")
st.markdown("---")

# Split screen workspace layout layout
col_form, col_metrics = st.columns([1, 2], gap="large")

with col_form:
    st.subheader("Configuration Input Module")
    with st.form("farm_input_form"):
        f_name = st.text_input("Farm / Field Name", value=st.session_state.current_farm["farm_name"])
        f_crop = st.selectbox("Crop Type", ["Wheat", "Rice", "Cotton", "Maize", "Sugarcane"])
        f_area = st.number_input("Field Area (Acres)", min_value=1.0, max_value=500.0, value=st.session_state.current_farm["field_area"])
        f_stage = st.selectbox("Growth Stage", ["Vegetative", "Flowering", "Ripening"])
        f_moisture = st.slider("Soil Moisture Content (%)", 0.0, 100.0, float(st.session_state.current_farm["soil_moisture"]))
        f_infestation = st.select_slider("Infestation Severity", options=["None", "Low", "Medium", "High"])
        
        submit = st.form_submit_button("Sync Configuration & Diagnostics")
        
        if submit:
            # Construct configuration
            record = {
                "farm_name": f_name, "crop_type": f_crop, "field_area": f_area,
                "growth_stage": f_stage, "soil_moisture": f_moisture, "infestation_level": f_infestation,
                "water_usage": round(f_area * 12.5, 2), "fertilizer_usage": round(f_area * 4.2, 2),
                "temperature": 32.0, "humidity": 60.0, "wind_speed": 10.5,
                "operational_cost": round(f_area * 8.5, 2), "yield_tons": round(f_area * 2.1, 2)
            }
            st.session_state.current_farm = record
            st.session_state.df = save_farm_record(record)
            st.success("Telemetry updated successfully!")

with col_metrics:
    st.subheader("Real-Time Telemetry Summary")
    
    # Top KPI Cards Row
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"<div class='metric-card'><b>Active Sector</b><br><h3>{st.session_state.current_farm['farm_name']}</h3></div>", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"<div class='metric-card'><b>Selected Crop</b><br><h3>{st.session_state.current_farm['crop_type']}</h3></div>", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"<div class='metric-card'><b>Target Area</b><br><h3>{st.session_state.current_farm['field_area']} Acres</h3></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress bars
    st.write("**Soil Moisture Level Monitoring Status**")
    st.progress(int(st.session_state.current_farm["soil_moisture"]))
    
    # Graphic visualization
    st.subheader("Historical Analytics Profile Breakdown")
    chart_df = st.session_state.df
    fig = px.bar(chart_df.tail(10), x="farm_name", y="field_area", color="crop_type", 
                 title="Recent Area Profiles by Asset Configurations", color_discrete_sequence=px.colors.sequential.Darkmint)
    st.plotly_chart(fig, use_container_width=True)
