import os
import pandas as pd
import numpy as np

DATA_PATH = "data/farm_data.csv"

def init_database():
    """Initializes a sample database if none exists."""
    if not os.path.exists("data"):
        os.makedirs("data")
        
    if not os.path.exists(DATA_PATH):
        # Generate dummy historical data for ML training and dashboarding
        np.random.seed(42)
        records = 200
        
        crops = ["Wheat", "Rice", "Cotton", "Maize", "Sugarcane"]
        stages = ["Vegetative", "Flowering", "Ripening"]
        
        data = {
            "farm_name": [f"Alpha Farm {i}" for i in range(records)],
            "crop_type": np.random.choice(crops, records),
            "field_area": np.random.uniform(5, 150, records).round(2),
            "growth_stage": np.random.choice(stages, records),
            "soil_moisture": np.random.uniform(20, 80, records).round(2),
            "infestation_level": np.random.choice(["None", "Low", "Medium", "High"], records, p=[0.4, 0.4, 0.15, 0.05]),
            "water_usage": np.random.uniform(100, 1000, records).round(2),
            "fertilizer_usage": np.random.uniform(20, 200, records).round(2),
            "temperature": np.random.uniform(18, 42, records).round(1),
            "humidity": np.random.uniform(30, 90, records).round(1),
            "wind_speed": np.random.uniform(2, 25, records).round(1),
            "operational_cost": np.random.uniform(50, 450, records).round(2),
            "yield_tons": np.random.uniform(1.5, 8.0, records).round(2)
        }
        
        df = pd.DataFrame(data)
        df.to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)

def save_farm_record(record_dict):
    """Appends a new user form configuration to the historical log."""
    df = init_database()
    new_df = pd.DataFrame([record_dict])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return df
