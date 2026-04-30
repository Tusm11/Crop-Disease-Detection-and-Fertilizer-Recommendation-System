"""
Rebuild the CNN model if it doesn't exist or is corrupted.
This runs on Streamlit startup to ensure a compatible model is available.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import os
import json

def rebuild_cnn_model():
    """Rebuild the CNN model with TensorFlow 2.15.1 compatible format."""
    
    model_path = 'models/plant_cnn_model.keras'
    
    # Check if model exists and is valid
    if os.path.exists(model_path):
        try:
            # Try to load it
            model = tf.keras.models.load_model(model_path)
            return model
        except Exception as e:
            print(f"Model loading failed: {e}")
            print("Rebuilding model...")
    
    # Load class names to get number of classes
    try:
        with open('models/class_names.json', 'r') as f:
            class_names = json.load(f)
        num_classes = len(class_names)
    except:
        num_classes = 59
    
    # Build new model
    model = models.Sequential([
        layers.Input(shape=(64, 64, 3)),
        layers.Rescaling(1./255),
        
        # Block 1
        layers.Conv2D(32, (3,3), activation='relu', padding='same'),
        layers.Conv2D(32, (3,3), activation='relu', padding='same'),
        layers.MaxPooling2D(2,2),
        layers.Dropout(0.25),
        
        # Block 2
        layers.Conv2D(64, (3,3), activation='relu', padding='same'),
        layers.Conv2D(64, (3,3), activation='relu', padding='same'),
        layers.MaxPooling2D(2,2),
        layers.Dropout(0.25),
        
        # Block 3
        layers.Conv2D(128, (3,3), activation='relu', padding='same'),
        layers.Conv2D(128, (3,3), activation='relu', padding='same'),
        layers.MaxPooling2D(2,2),
        layers.Dropout(0.25),
        
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Try to load weights from .h5 file if it exists
    h5_path = 'models/plant_cnn_model.h5'
    if os.path.exists(h5_path):
        try:
            old_model = tf.keras.models.load_model(h5_path)
            weights = old_model.get_weights()
            if len(weights) == len(model.get_weights()):
                model.set_weights(weights)
                print("✓ Weights loaded from .h5 file")
        except Exception as e:
            print(f"Could not load weights from .h5: {e}")
    
    # Save the rebuilt model
    model.save(model_path)
    print(f"✓ Model rebuilt and saved to {model_path}")
    
    return model

if __name__ == "__main__":
    rebuild_cnn_model()
