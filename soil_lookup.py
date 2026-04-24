"""
Soil type lookup - provides sample values for each soil type + crop combination
Based on fertilizer_recommendation.csv
"""
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('fertilizer_recommendation.csv')

def get_soil_crop_values(soil_type, crop_type):
    """
    Get sample values for a specific soil type and crop combination.
    Returns dict with N, P, K, Temperature, Humidity, Soil_Moisture
    
    Instead of using averages (which scale to ~0), we sample from actual data.
    """
    # Filter by soil type and crop type
    filtered = df[(df['Soil_Type'] == soil_type) & (df['Crop_Type'] == crop_type)]
    
    # If no exact match, try just soil type
    if filtered.empty:
        filtered = df[df['Soil_Type'] == soil_type]
    
    # If still no match, use defaults
    if filtered.empty:
        return {
            'N': 60,
            'P': 40,
            'K': 60,
            'Temperature': 25.0,
            'Humidity': 65.0,
            'Soil_Moisture': 35.0
        }
    
    # Randomly sample one row
    sample = filtered.sample(n=1, random_state=np.random.randint(0, 10000)).iloc[0]
    
    return {
        'N': int(sample['Nitrogen_Level']),
        'P': int(sample['Phosphorus_Level']),
        'K': int(sample['Potassium_Level']),
        'Temperature': float(sample['Temperature']),
        'Humidity': float(sample['Humidity']),
        'Soil_Moisture': float(sample['Soil_Moisture'])
    }

def get_available_soil_types():
    """Return list of available soil types"""
    return sorted(df['Soil_Type'].unique().tolist())
