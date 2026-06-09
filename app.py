import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AgriDrone VRA Dashboard",
    page_icon="🛸",
    layout="wide"
)

st.title("🛸 Drone Spraying & Resource Optimizer")
st.markdown("""
This dashboard simulates how ICT-driven drone systems process multi-spectral field data, 
visualize crop health indices, and calculate variable-rate spraying prescriptions.
""")

st.sidebar.header("🕹️ Field & Drone Controls")

# -----------------------------------------------------------------------------
# 2. SIDEBAR CONFIGURATIONS
# -----------------------------------------------------------------------------
field_size = st.sidebar.slider("Simulated Field Resolution (NxN Grid)", 20, 100, 50, step=10)
infestation_risk = st.sidebar.slider("Simulated Crop Stress / Weed Intensity", 0.1, 1.0, 0.5, 0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("💧 Variable-Rate Calibration")
base_chemical_rate = st.sidebar.number_input("Base Input Fluid Rate (L/Hectare)", value=2.5, step=0.5)
base_water_rate = st.sidebar.number_input("Base Water Volume (L/Hectare)", value=100.0, step=10.0)
ulv_mode = st.sidebar.toggle("Enable Ultra-Low Volume (ULV) Atomization", value=True)

# -----------------------------------------------------------------------------
# 3. REMOTE SENSING DATA ENGINE (NDVI GENERATOR)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=60)
def generate_synthetic_field(size, stress):
    """Simulates Near-Infrared (NIR) and Red band data to compute NDVI."""
    np.random.seed(42) # Static seed for predictable field boundaries
    
    # Generate mock topography/soil variances using coordinate gradients
    x = np.linspace(-2, 2, size)
    y = np.linspace(-2, 2, size)
    X, Y = np.meshgrid(x, y)
    z = np.sin(X) * np.cos(Y) + np.random.normal(0, 0.25, (size, size))
    
    # Normalize mapping between 0.0 and 1.0
    z_norm = (z - z.min()) / (z.max() - z.min())
    
    # Simulate spectral reflectance response 
    # High stress forces higher Red absorption loss and lower NIR structural reflection
    red = 0.05 + 0.35 * (z_norm * stress)
    nir = 0.85 - 0.45 * (z_norm * stress)
    
    # Compute NDVI = (NIR - RED) / (NIR + RED)
    ndvi = (nir - red) / (nir + red)
    return np.clip(ndvi, -1.0, 1.0)

ndvi_matrix = generate_synthetic_field(field_size, infestation_risk)

# -----------------------------------------------------------------------------
# 4. PRESCRIPTION ALGORITHM (VARIABLE-RATE ENGINE)
# -----------------------------------------------------------------------------
# Define critical agronomic threshold where remediation is required
CRITICAL_HEALTH_THRESHOLD = 0.50

# Flatten grid arrays for vector calculation and tracking dataframe conversion
grid_x, grid_y = np.indices(ndvi_matrix.shape)
df = pd.DataFrame({
    "X_Coord_m": grid_x.flatten() * 2,  # Scaled to represent meter tracking spacing
    "Y_Coord_m": grid_y.flatten() * 2,
    "NDVI": ndvi_matrix.flatten()
})

def calculate_vra_dosage(row):
    """Applies inverse logic: Lower crop health (NDVI) requires heavier chemical delivery."""
    if row["NDVI"] >= CRITICAL_HEALTH_THRESHOLD:
        # Healthy canopy: Drop application to minimal baseline protection volume
        chem_factor = 0.15 
        water_factor = 0.20
    else:
        # Compromised canopy: Scale application up progressively based on stress
        chem_factor = 1.3 - row["NDVI"]
        water_factor = 1.1
        
    # Scale raw totals to match individual grid square areas
    chem_dose = base_chemical_rate * chem_factor * 0.01 
    water_dose = base_water_rate * water_factor * 0.01
    
    # Apply ULV mechanical hardware efficiency deduction
    if ulv_mode:
        water_dose *= 0.15  # Droplet atomization cuts carrier water demand up to 85%
        
    return pd.Series([chem_dose, water_dose])

df[["Target_Chemical_L", "Target_Water_L"]] = df.apply(calculate_vra_dosage, axis=1)

# -----------------------------------------------------------------------------
# 5. KPIS & METRIC METADATA CALCULATIONS
# -----------------------------------------------------------------------------
total_chem = df["Target_Chemical_L"].sum()
total_water = df["Target_Water_L"].sum()

# Baseline benchmarks calculating standard blanket/uniform coverage configurations
blanket_chem = (base_chemical_rate * 1.1) * 0.01 * len(df)
blanket_water = base_water_rate * 0.01 * len(df)

saved_chem_pct = max(0.0, (1.0 - (total_chem / blanket_chem)) * 100)
saved_water_pct = max(0.0, (1.0 - (total_water / blanket_water)) * 100)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Chemical Required", f"{total_chem:.2f} L")
with col2:
    st.metric("Total Water Required", f"{total_water:.1f} L")
with col3:
    st.metric("Chemical Waste Saved", f"{saved_chem_pct:.1f}%", delta="Optimized")
with col4:
    st.metric("Water Footprint Saved", f"{saved_water_pct:.1f}%", delta="ULV Active" if ulv_mode else None)

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. SPATIAL GEOMETRY VISUALIZATIONS
# -----------------------------------------------------------------------------
map_col1, map_col2 = st.columns(2)

with map_col1:
    st.subheader("🌾 Crop Canopy Health Map (NDVI)")
    fig_ndvi = px.imshow(
        ndvi_matrix,
        color_continuous_scale="RdYlGn",  # Standard agronomic color ramp
        labels=dict(x="Field Grid Columns", y="Field Grid Rows", color="NDVI Index"),
        origin="lower"
    )
    fig_ndvi.update_layout(height=450, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_ndvi, use_container_width=True)
    st.caption("Interpretation: Red/Yellow patches signal heavy stress anomalies or weed growth zones.")

with map_col2:
    st.subheader("🎯 Drone Flow-Rate Prescription Map")
    fig_spray = px.scatter(
        df,
        x="X_Coord_m",
        y="Y_Coord_m",
        color="Target_Chemical_L",
        size=df["Target_Chemical_L"].clip(lower=0.005),
        color_continuous_scale="Purples",
    )
    fig_spray.update_layout(height=450, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_spray, use_container_width=True)
    st.caption("Interpretation: Dynamic dosage values mapped to spatial target coordinates.")

# -----------------------------------------------------------------------------
# 7. TELEMETRY LOG FILE EXPORT GENERATOR
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("📋 Drone Mission Telemetry Log Export")
st.markdown("This structured vector list format can be downloaded directly and synced to commercial drone flight mission control software.")

# Present a clean subset of the target matrix log
st.dataframe(df, use_container_width=True, hide_index=True)
