import streamlit as st
import numpy as np

st.title("🌤️ Real-Time Weather Intelligence System")
st.markdown("---")

col_w, col_rec = st.columns(2)

with col_w:
    st.subheader("Atmospheric Matrix Controls")
    temp = st.slider("Temperature (°C)", 10, 50, int(st.session_state.current_farm["temperature"]))
    humidity = st.slider("Relative Humidity (%)", 10, 100, int(st.session_state.current_farm["humidity"]))
    wind = st.slider("Wind Velocity (km/h)", 0, 40, int(st.session_state.current_farm["wind_speed"]))

with col_rec:
    st.subheader("Flight Operational Readiness Diagnostics")
    
    # Decision Matrix Evaluation logic
    if wind > 20:
        st.error("🚨 CRITICAL WARNING: Wind speed exceeds flight threshold limits. High drift and crash risk. Suspend missions.")
    elif temp > 38 and humidity < 30:
        st.warning("⚠️ RISK WARNING: Severe evaporation rate detected. Fluid delivery efficiency significantly impaired.")
    elif wind > 12:
        st.info("ℹ️ CAUTION ALERT: Moderate cross-winds detected. Adjust flight velocity downward and scale payload weights.")
    else:
        st.success("✅ OPTIMAL CONDITIONS: Environment cleared for safe standard spraying applications.")
