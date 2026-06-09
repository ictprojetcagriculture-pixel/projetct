import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🌱 Crop Health Analytics & NDVI Core")
st.markdown("---")

st.subheader("Simulated Multispectral Canopy Map")
st.info("Visual representation of normalized variance vegetative indices (NDVI) derived from simulation parameters.")

# Generate pseudo spatial array matrices
np.random.seed(42)
grid_size = 50
health_matrix = np.random.rand(grid_size, grid_size)

# Apply skewing factor based on historical user variables configuration
if st.session_state.current_farm["infestation_level"] == "High":
    health_matrix *= 0.4
elif st.session_state.current_farm["infestation_level"] == "Medium":
    health_matrix *= 0.7
else:
    health_matrix *= 0.95

# Plot canvas layout rendering logic
fig, ax = plt.subplots(figsize=(10, 4))
im = ax.imshow(health_matrix, cmap="RdYlGn", origin="lower")
fig.colorbar(im, label="NDVI Scale (0.0 Dead -> 1.0 Optimal Health)")
ax.axis('off')
st.pyplot(fig)

# Smart Diagnostics feedback recommendation engines
st.subheader("AI Automated Directives Engine")
if st.session_state.current_farm["infestation_level"] in ["High", "Medium"]:
    st.markdown("""> **IMMEDIATE DIRECTIVE:** Concentrated hotspot clusters detected in Sector Quad-3. Deploy precision Drone Pesticide trajectory arrays immediately to isolate vector expansions.""")
else:
    st.markdown("""> **SYSTEM DIRECTIVE:** Overall canopy indices are within normal operational margins. Continue standard scheduled macro-fertilization routing operations.""")
