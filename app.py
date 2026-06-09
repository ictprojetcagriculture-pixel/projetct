import streamlit as st
from modules.database import init_database

# Configure view properties
st.set_page_config(
    page_title="AgriDrone OS",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Custom CSS styling injection
st.markdown("""
    <style>
    :root {
        --primary-color: #2E7D32;
        --background-color: #F1F8E9;
    }
    .stApp {
        background-color: #FCFDFB;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #2E7D32;
    }
    h1, h2, h3 {
        color: #1B5E20;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session Data Store
if 'df' not in st.session_state:
    st.session_state.df = init_database()
if 'current_farm' not in st.session_state:
    st.session_state.current_farm = {
        "farm_name": "Green Valley Base",
        "crop_type": "Wheat",
        "field_area": 45.0,
        "growth_stage": "Vegetative",
        "soil_moisture": 42.5,
        "infestation_level": "Low",
        "water_usage": 350.0,
        "fertilizer_usage": 75.0,
        "temperature": 28.5,
        "humidity": 55.0,
        "wind_speed": 12.0
    }

# Define Page Architecture Structure Navigation 
pages = {
    "Operations Control": [
        st.Page("pages/dashboard.py", title="Command Dashboard", icon="📊"),
        st.Page("pages/drone_optimizer.py", title="Flight Path Optimizer", icon="🛸")
    ],
    "Environmental Intelligence": [
        st.Page("pages/weather.py", title="Weather Intelligence", icon="🌤️"),
        st.Page("pages/crop_health.py", title="Crop Health Core", icon="🌱"),
        st.Page("pages/analytics.py", title="Predictive Analytics", icon="📈")
    ]
}

pg = st.navigation(pages)
pg.run()
