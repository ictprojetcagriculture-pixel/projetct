import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & THEMING
# ==============================================================================
st.set_page_config(
    page_title="AgriTech ICT - Smart Agriculture Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional dark gray, white, and agricultural green aesthetic
st.markdown("""
    <style>
        /* Main background and text */
        .stApp {
            background-color: #f8f9fa;
        }
        h1, h2, h3 {
            color: #1e3d2f !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1e3d2f;
            color: #ffffff;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        /* Metric card custom styling border */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border-left: 5px solid #2e7d32;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        /* Button styling */
        .stButton>button {
            background-color: #2e7d32 !important;
            color: white !important;
            border-radius: 5px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #1b5e20 !important;
            color: white !important;
        }
    </style>
""", unsafe_style_html=True)


# ==============================================================================
# 2. NAVIGATION SIDEBAR
# ==============================================================================
st.sidebar.title("🌱 AgriTech ICT")
st.sidebar.markdown("Transforming farming through Information & Communication Technology.")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate Menu",
