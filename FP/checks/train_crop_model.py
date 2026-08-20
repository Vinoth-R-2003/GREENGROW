"""
Training script for the Custom Crop Prediction ML model.

Generates a realistic synthetic dataset linking Temperature, Rainfall, and Soil Type
to optimal crops, and trains a RandomForestClassifier pipeline using scikit-learn.

Usage:
    python checks/train_crop_model.py

The trained model is saved to checks/ml_models/crop_prediction_model.pkl
"""

import os
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def generate_synthetic_data(num_samples=2000):
    np.random.seed(42)
    
    # Define crop profiles: (Temp mean, Rain mean, Soil types)
    profiles = {
        'Rice': {'temp_mean': 28, 'temp_std': 4, 'rain_mean': 2000, 'rain_std': 300, 'soils': ['Clay', 'Loamy', 'Clay Loam']},
        'Wheat': {'temp_mean': 20, 'temp_std': 5, 'rain_mean': 800, 'rain_std': 150, 'soils': ['Loamy', 'Clay', 'Sandy Loam']},
        'Maize': {'temp_mean': 25, 'temp_std': 5, 'rain_mean': 1000, 'rain_std': 200, 'soils': ['Loamy', 'Sandy', 'Clay Loam']},
        'Cotton': {'temp_mean': 30, 'temp_std': 4, 'rain_mean': 600, 'rain_std': 150, 'soils': ['Sandy', 'Loamy', 'Black']},
        'Coffee': {'temp_mean': 22, 'temp_std': 3, 'rain_mean': 1800, 'rain_std': 250, 'soils': ['Loamy', 'Laterite']},
        'Apple': {'temp_mean': 15, 'temp_std': 4, 'rain_mean': 1200, 'rain_std': 200, 'soils': ['Loamy', 'Silt']},
        'Grapes': {'temp_mean': 24, 'temp_std': 5, 'rain_mean': 600, 'rain_std': 100, 'soils': ['Sandy', 'Loamy', 'Gravelly']},
        'Potato': {'temp_mean': 18, 'temp_std': 4, 'rain_mean': 900, 'rain_std': 150, 'soils': ['Sandy', 'Loamy', 'Peaty']},
        'Sugarcane': {'temp_mean': 32, 'temp_std': 3, 'rain_mean': 2200, 'rain_std': 400, 'soils': ['Clay', 'Loamy', 'Alluvial']},
        'Tea': {'temp_mean': 20, 'temp_std': 3, 'rain_mean': 2000, 'rain_std': 300, 'soils': ['Loamy', 'Laterite']},
        'Barley': {'temp_mean': 18, 'temp_std': 5, 'rain_mean': 500, 'rain_std': 150, 'soils': ['Sandy', 'Loamy']},
        'Tomato': {'temp_mean': 24, 'temp_std': 4, 'rain_mean': 800, 'rain_std': 200, 'soils': ['Loamy', 'Sandy Loam']},
    }
    
    data = []
    
    for _ in range(num_samples):
        crop = np.random.choice(list(profiles.keys()))
        prof = profiles[crop]
        
        temp = np.random.normal(prof['temp_mean'], prof['temp_std'])
        rain = np.random.normal(prof['rain_mean'], prof['rain_std'])
        soil = np.random.choice(prof['soils'])
        
        data.append({
            'Temperature': round(temp, 1),
            'Rainfall': round(max(0, rain), 1), # Rain can't be negative
            'Soil_Type': soil.lower(), # Normalize to lowercase
            'Crop': crop
        })
        
    return pd.DataFrame(data)

def train_model(output_path=None):
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, 'ml_models', 'crop_prediction_model.pkl')
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("[INFO] Generating synthetic agricultural dataset (3000 samples)...")
    df = generate_synthetic_data(3000)
    
    X = df[['Temperature', 'Rainfall', 'Soil_Type']]
    y = df['Crop']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("[INFO] Building and training Pipeline (OneHotEncoder + RandomForest)...")
    
    # We use a pipeline to handle the categorical Soil_Type column automatically
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['Soil_Type'])
        ],
        remainder='passthrough'
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    
    accuracy = pipeline.score(X_test, y_test)
    print(f"[INFO] Model Accuracy on test set: {accuracy:.4f}")
    
    print(f"[INFO] Saving model to: {os.path.basename(output_path)}")
    joblib.dump(pipeline, output_path)
    print("[INFO] Training complete! You can now use this model for fast offline predictions.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train the Crop Prediction ML model')
    parser.add_argument('--output', type=str, default=None, help='Output path for the trained model (.pkl)')
    args = parser.parse_args()
    
    train_model(args.output)
