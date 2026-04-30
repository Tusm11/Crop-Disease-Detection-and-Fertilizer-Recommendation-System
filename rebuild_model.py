import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Load the old model (ignore the augmentation layer errors)
print("Loading old model...")
try:
    old_model = tf.keras.models.load_model('models/plant_cnn_model.keras')
    print("✓ Old model loaded")
except Exception as e:
    print(f"✗ Could not load old model: {e}")
    exit(1)

# Get the weights
print("Extracting weights...")
old_weights = old_model.get_weights()
print(f"✓ Extracted {len(old_weights)} weight arrays")

# Build a NEW model WITHOUT augmentation layers (inference only)
print("Building new inference model...")
IMG_SIZE = (64, 64)
num_classes = old_model.output_shape[-1]

new_model = models.Sequential([
    layers.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
    
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

print("✓ New model built")

# Transfer ALL weights (the new model should have same number)
print(f"Transferring {len(old_weights)} weights...")
new_model.set_weights(old_weights)
print("✓ Weights transferred")

# Save as .keras
new_model.save('models/plant_cnn_model.keras')
print("✓ Model saved to models/plant_cnn_model.keras")

# Test loading
print("Testing load...")
test_model = tf.keras.models.load_model('models/plant_cnn_model.keras')
print("✓ Model loads successfully!")
print(f"✓ Output shape: {test_model.output_shape}")
