import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

MODEL_DIR = "models"

class AgriPredictor:
    def __init__(self):
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        self.le_crop = LabelEncoder()
        self.le_stage = LabelEncoder()
        self.yield_model = None
        self.cost_model = None
        
    def train_models(self, df):
        """Fits Random Forest models based on database records."""
        df_encoded = df.copy()
        
        # Fit label encoders safely
        df_encoded['crop_type'] = self.le_crop.fit_transform(df_encoded['crop_type'])
        df_encoded['growth_stage'] = self.le_stage.fit_transform(df_encoded['growth_stage'])
        
        # Define features
        X_yield = df_encoded[['field_area', 'crop_type', 'water_usage', 'fertilizer_usage', 'temperature']]
        y_yield = df_encoded['yield_tons']
        
        X_cost = df_encoded[['field_area', 'crop_type', 'fertilizer_usage', 'water_usage']]
        y_cost = df_encoded['operational_cost']
        
        # Train
        self.yield_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.yield_model.fit(X_yield, y_yield)
        
        self.cost_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.cost_model.fit(X_cost, y_cost)
        
        # Save assets
        joblib.dump(self.yield_model, f"{MODEL_DIR}/yield_model.pkl")
        joblib.dump(self.cost_model, f"{MODEL_DIR}/cost_model.pkl")
        joblib.dump(self.le_crop, f"{MODEL_DIR}/le_crop.pkl")
        joblib.dump(self.le_stage, f"{MODEL_DIR}/le_stage.pkl")

    def load_or_train(self, df):
        try:
            self.yield_model = joblib.load(f"{MODEL_DIR}/yield_model.pkl")
            self.cost_model = joblib.load(f"{MODEL_DIR}/cost_model.pkl")
            self.le_crop = joblib.load(f"{MODEL_DIR}/le_crop.pkl")
            self.le_stage = joblib.load(f"{MODEL_DIR}/le_stage.pkl")
        except:
            self.train_models(df)

    def predict(self, area, crop, water, fertilizer, temp):
        try:
            crop_enc = self.le_crop.transform([crop])[0]
        except:
            crop_enc = 0 # Fallback for unseen inputs
            
        features_yield = np.array([[area, crop_enc, water, fertilizer, temp]])
        features_cost = np.array([[area, crop_enc, fertilizer, water]])
        
        pred_yield = self.yield_model.predict(features_yield)[0]
        pred_cost = self.cost_model.predict(features_cost)[0]
        
        return round(pred_yield * area, 2), round(pred_cost * area, 2)
