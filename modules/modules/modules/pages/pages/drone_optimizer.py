import streamlit as st
import folium
from streamlit_folium import st_folium
from modules.optimizer import calculate_drone_metrics

st.title("🛸 Autonomous Drone Spraying & Path Optimizer")
st.markdown("---")

col_params, col_results = st.columns([1, 2])

with col_params:
    st.subheader("Mission Design Parameters")
    spray_mode = st.selectbox("Target Treatment Type", ["Pesticide", "Fertilizer", "Water"])
    tank_cap = st.slider("Payload Tank Capacity (Liters)", 10, 50, 20)
    flight_speed = st.slider("Target Ground Speed (m/s)", 2, 15, 8)
    bat_cap = st.slider("Battery Module Pack Capacity (Ah)", 10, 30, 16)
    
    # Core optimization trigger execution
    metrics = calculate_drone_metrics(
        st.session_state.current_farm["field_area"],
        spray_mode, tank_cap, flight_speed, bat_cap
    )

with col_results:
    st.subheader("Calculated Flight Logistics Metrics")
    
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Required Fluid Payload", f"{metrics['total_volume']} L")
    r2.metric("Flight Distance Traveled", f"{metrics['flight_distance_km']} km")
    r3.metric("Estimated Spray Time", f"{metrics['flight_time_min']} mins")
    r4.metric("Refill Cycles Required", f"{metrics['refills']}")
    
    # Efficiency Resource Engine Visualization
    st.subheader("Resource Conservation (vs Traditional Operations)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Water Saved", f"{metrics['savings_water']}%", delta="Reduction")
    c2.metric("Time Saved", f"{metrics['savings_time']}%", delta="Reduction")
    c3.metric("Financial Cost Reduction", f"{metrics['savings_cost']}%", delta="Savings")

st.markdown("---")
st.subheader("Interactive Mission Path Boundaries Canvas")

# Build coordinate maps around simulated Wah / Taxila base areas
lat, lon = 33.7743, 72.7521
m = folium.Map(location=[lat, lon], zoom_start=15, tiles="OpenStreetMap")

# Generate bounding box based on user selected area constraints
coords = [
    [lat - 0.003, lon - 0.003],
    [lat - 0.003, lon + 0.003],
    [lat + 0.003, lon + 0.003],
    [lat + 0.003, lon - 0.003]
]

# Draw Farm boundary perimeter
folium.Polygon(locations=coords, color="green", weight=3, fill=True, fill_opacity=0.15, popup="Target Field Boundary").add_to(m)

# Generate simulated flight pathways vectors
for i in range(len(coords)-1):
    folium.PolyLine(locations=[coords[i], coords[i+1]], color="cyan", weight=2.5, opacity=0.8, tooltip="Drone Path Swath").add_to(m)

st_folium(m, width=1100, height=450)
