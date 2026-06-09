import streamlit as st
import pandas as pd
from modules.ml_engine import AgriPredictor

st.title("📈 Machine Learning Core Predictive Modeling Analytics")
st.markdown("---")

predictor = AgriPredictor()
# Seed models dynamically using cache states
predictor.load_or_train(st.session_state.df)

st.subheader("Yield and Operational Overhead Forecasting Matrix")
st.write("Outputs driven by Scikit-Learn Random Forest Regressor models trained on production historical logs.")

farm = st.session_state.current_farm

# Compute predictions using current session state memory inputs
predicted_yield, predicted_cost = predictor.predict(
    farm["field_area"],
    farm["crop_type"],
    farm["water_usage"],
    farm["fertilizer_usage"],
    farm["temperature"]
)

c1, c2 = st.columns(2)
with c1:
    st.metric(label="Predicted Yield Forecast Output", value=f"{predicted_yield} Metric Tons")
with c2:
    st.metric(label="Projected Operational Overhead Expense", value=f"${predicted_cost}")

# Data Output Export Engine
st.markdown("---")
st.subheader("Export Center Log Analytics")

csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Export Complete Historical Telemetry Logs to CSV Format",
    data=csv_data,
    file_name="historical_agri_drone_telemetry_report.csv",
    mime="text/csv"
)
