"""
Convert Keras 3.14.0 model to TensorFlow 2.15.1 compatible format.
This script loads the old model, extracts weights, and rebuilds without augmentation layers.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import json
import os

print("=" * 60)
print("Converting model to TensorFlow 2.15.1 compatible format")
print("=" * 60)

# Load class names
with open('models/class_names.json', 'r') as f:
    class_names = json.load(f)

num_classes = len(class_names)
print(f"Number of classes: {num_classes}")

# Try to load the old model
old_model_path = 'models/plant_cnn_model.keras'
print(f"\nLoading old model from: {old_model_path}")

try:
    # Load with custom_objects to handle any custom layers
    old_model = tf.keras.models.load_model(old_model_path)
    print("✓ Old model loaded successfully")
except Exception as e:
    print(f"✗ Could not load old model: {e}")
    print("\nTrying alternative: loading from .h5 file...")
    try:
        old_model = tf.keras.models.load_model('models/plant_cnn_model.h5')
        print("✓ Loaded from .h5 file")
    except Exception as e2:
        print(f"✗ Could not load from .h5 either: {e2}")
        exit(1)

print(f"Old model summary:")
old_model.summary()

# Extract weights from the old model
print("\nExtracting weights from old model...")
old_weights = old_model.get_weights()
print(f"✓ Extracted {len(old_weights)} weight arrays")

# Build new model WITHOUT augmentation layers
# Augmentation should be done at inference time, not in the model
print("\nBuilding new inference model (without augmentation layers)...")

new_model = models.Sequential([
    layers.Input(shape=(64, 64, 3)),
    
    # Rescaling (this stays in the model)
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
print(f"New model has {len(new_model.get_weights())} weight arrays")

# The old model has augmentation layers at the beginning
# We need to skip those and only transfer the actual network weights
# Augmentation layers: RandomFlip, RandomRotation, RandomZoom, RandomBrightness, RandomContrast = 5 layers
# Then Rescaling = 1 layer
# So we skip the first 6 layers (5 augmentation + 1 rescaling) and start from layer 6

print("\nTransferring weights...")
print(f"Old model weights: {len(old_weights)}")
print(f"New model weights: {len(new_model.get_weights())}")

# The old model structure:
# 0-4: Augmentation layers (no weights)
# 5: Rescaling (no weights)
# 6+: Actual network layers (with weights)

# Count weights in old model by layer
weight_idx = 0
for i, layer in enumerate(old_model.layers):
    layer_weights = layer.get_weights()
    if layer_weights:
        print(f"  Layer {i} ({layer.name}): {len(layer_weights)} weight arrays")
        weight_idx += len(layer_weights)

# Transfer weights - skip augmentation layers
# The new model starts directly with Rescaling, then the network
# So we need to map old weights to new weights, skipping augmentation

# Find where the actual network weights start in the old model
old_layer_idx = 0
old_weight_idx = 0
for i, layer in enumerate(old_model.layers):
    if 'random' in layer.name.lower() or 'rescaling' in layer.name.lower():
        # Skip augmentation and rescaling layers
        old_layer_idx = i + 1
    else:
        break

print(f"\nSkipping first {old_layer_idx} layers (augmentation + rescaling)")

# Collect weights from actual network layers
network_weights = []
for layer in old_model.layers[old_layer_idx:]:
    network_weights.extend(layer.get_weights())

print(f"Network weights collected: {len(network_weights)}")
print(f"New model expects: {len(new_model.get_weights())}")

if len(network_weights) == len(new_model.get_weights()):
    new_model.set_weights(network_weights)
    print("✓ Weights transferred successfully")
else:
    print(f"⚠ Weight count mismatch!")
    print(f"  Old network: {len(network_weights)} weights")
    print(f"  New model: {len(new_model.get_weights())} weights")
    print("\nAttempting to match by layer...")
    
    # Try to match layer by layer
    new_layer_idx = 1  # Skip Input layer
    old_layer_idx_start = old_layer_idx
    
    for new_layer in new_model.layers[1:]:  # Skip Input
        if new_layer.get_weights():
            # Find corresponding old layer
            old_layer = old_model.layers[old_layer_idx_start]
            old_weights_layer = old_layer.get_weights()
            
            if old_weights_layer and len(old_weights_layer) == len(new_layer.get_weights()):
                new_layer.set_weights(old_weights_layer)
                print(f"  ✓ {new_layer.name} <- {old_layer.name}")
                old_layer_idx_start += 1
            else:
                print(f"  ✗ Could not match {new_layer.name}")
                old_layer_idx_start += 1

# Compile the new model
new_model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("\n✓ New model compiled")

# Save in multiple formats for compatibility
print("\nSaving model in multiple formats...")

# Save as .keras (TF 2.15.1 format)
new_model.save('models/plant_cnn_model_tf215.keras')
print("✓ Saved as: models/plant_cnn_model_tf215.keras")

# Save as SavedModel format (most compatible)
new_model.export('models/plant_cnn_model_savedmodel')
print("✓ Saved as: models/plant_cnn_model_savedmodel/")

# Save as .h5 (legacy format)
new_model.save('models/plant_cnn_model_tf215.h5')
print("✓ Saved as: models/plant_cnn_model_tf215.h5")

# Test loading
print("\nTesting model loading...")
try:
    test_model = tf.keras.models.load_model('models/plant_cnn_model_tf215.keras')
    print("✓ Successfully loaded .keras model")
except Exception as e:
    print(f"✗ Failed to load .keras model: {e}")

try:
    test_model = tf.keras.models.load_model('models/plant_cnn_model_savedmodel')
    print("✓ Successfully loaded SavedModel")
except Exception as e:
    print(f"✗ Failed to load SavedModel: {e}")

print("\n" + "=" * 60)
print("Conversion complete!")
print("=" * 60)
print("\nNext steps:")
print("1. Update app.py to load from 'models/plant_cnn_model_tf215.keras'")
print("2. Or use SavedModel: tf.keras.models.load_model('models/plant_cnn_model_savedmodel')")
print("3. Push to GitHub")
print("4. Streamlit Cloud will auto-rebuild")
