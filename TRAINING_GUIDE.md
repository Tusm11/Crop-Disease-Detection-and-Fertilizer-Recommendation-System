# Model Training Guide

This guide explains how to train both the CNN and AdaBoost models from scratch.

## Prerequisites

- Python 3.10+
- GPU (optional, but recommended for CNN training)
- Dataset folder with plant leaf disease images

## CNN Model Training

### Step 1: Prepare Dataset

The CNN model expects images organized in the following structure:

```
dataset/Plant_leave_diseases_dataset_without_augmentation/
├── Apple___Apple_scab/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Apple___Black_rot/
│   └── ...
├── Corn___Cercospora_leaf_spot/
│   └── ...
└── ... (59 disease classes total)
```

**Dataset sources:**
- [PlantVillage Dataset](https://github.com/spMohanty/PlantVillage-Dataset)
- [Kaggle Plant Disease Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)

### Step 2: Install Dependencies

```bash
pip install tensorflow==2.15.1 numpy pillow opencv-python
```

### Step 3: Run Training Script

```bash
python train_cnn.py
```

**What the script does:**
1. Loads images from `dataset/Plant_leave_diseases_dataset_without_augmentation/`
2. Splits data into 80% training, 20% validation
3. Applies data augmentation (flip, rotation, zoom, brightness, contrast)
4. Trains the CNN model for up to 15 epochs
5. Uses early stopping if validation accuracy plateaus
6. Saves the trained model to `models/plant_cnn_model.keras`

**Training time:**
- CPU: ~30-45 minutes
- GPU (NVIDIA): ~5-10 minutes

### Step 4: Monitor Training

The script outputs:
- Epoch-by-epoch accuracy and loss
- Best validation accuracy
- Training time

Example output:
```
AGRI-SMART CNN — Multi-class Disease Classifier
Classes: 59
Image size: (64, 64)
Class names saved.

TRAINING STARTED
Epoch 1/15
... training progress ...
Epoch 12/15 - Early stopping triggered
Done in 8.5 min
Best val accuracy: 92.34%
Model saved->models/plant_cnn_model.keras
```

### Step 5: Verify Model

Test the trained model:

```python
import tensorflow as tf
import json

# Load model
model = tf.keras.models.load_model('models/plant_cnn_model.keras')

# Load class names
with open('models/class_names.json') as f:
    class_names = json.load(f)

print(f"Model loaded successfully!")
print(f"Number of classes: {len(class_names)}")
print(f"Model output shape: {model.output_shape}")
```

## AdaBoost Model Training

### Step 1: Prepare Dataset

The AdaBoost model uses the `fertilizer_recommendation.csv` file which should contain:

```csv
Soil_Type,Crop_Type,Nitrogen_Level,Phosphorus_Level,Potassium_Level,Temperature,Humidity,Soil_Moisture,Fertilizer_Type
Loamy,Tomato,50,30,20,25,60,50,NPK_10_10_10
Sandy,Corn,60,40,30,28,55,45,NPK_20_20_20
...
```

**Columns:**
- `Soil_Type`: Loamy, Sandy, Clay, etc.
- `Crop_Type`: Tomato, Corn, Potato, etc.
- `Nitrogen_Level`: 0-100 (ppm)
- `Phosphorus_Level`: 0-100 (ppm)
- `Potassium_Level`: 0-100 (ppm)
- `Temperature`: 0-50 (°C)
- `Humidity`: 0-100 (%)
- `Soil_Moisture`: 0-100 (%)
- `Fertilizer_Type`: Target fertilizer recommendation

### Step 2: Install Dependencies

```bash
pip install scikit-learn pandas numpy joblib
```

### Step 3: Run Training Notebook

Open and run `adaboost.ipynb`:

```bash
jupyter notebook adaboost.ipynb
```

**Notebook sections:**
1. **Data Loading**: Load and explore the dataset
2. **Data Preprocessing**: Encode categorical variables, scale features
3. **Model Training**: Train AdaBoost classifier
4. **Model Evaluation**: Cross-validation, accuracy metrics
5. **Model Saving**: Save model and encoders

### Step 4: Training Process

The notebook performs:

```python
# 1. Load data
df = pd.read_csv('fertilizer_recommendation.csv')

# 2. Encode categorical variables
le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_fert = LabelEncoder()

# 3. Scale numeric features
scaler = StandardScaler()

# 4. Train AdaBoost
from sklearn.ensemble import AdaBoostClassifier
ada_model = AdaBoostClassifier(n_estimators=50, learning_rate=1.0)
ada_model.fit(X_train, y_train)

# 5. Evaluate
accuracy = ada_model.score(X_test, y_test)

# 6. Save
joblib.dump(ada_model, 'models/fertilizer_ada_model.pkl')
joblib.dump(le_soil, 'models/le_soil.pkl')
joblib.dump(le_crop, 'models/le_crop.pkl')
joblib.dump(le_fert, 'models/le_fert.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
```

### Step 5: Verify Model

Test the trained model:

```python
import joblib
import pandas as pd

# Load model and encoders
ada_model = joblib.load('models/fertilizer_ada_model.pkl')
le_soil = joblib.load('models/le_soil.pkl')
le_crop = joblib.load('models/le_crop.pkl')
le_fert = joblib.load('models/le_fert.pkl')
scaler = joblib.load('models/scaler.pkl')

# Make prediction
soil_enc = le_soil.transform(['Loamy'])[0]
crop_enc = le_crop.transform(['Tomato'])[0]
numeric_vals = [50, 30, 20, 25, 60, 50]  # N, P, K, Temp, Humidity, Moisture
numeric_scaled = scaler.transform([numeric_vals])[0]

X = [[*numeric_scaled, soil_enc, crop_enc]]
pred_idx = ada_model.predict(X)[0]
fertilizer = le_fert.inverse_transform([pred_idx])[0]

print(f"Recommended fertilizer: {fertilizer}")
```

## Hyperparameter Tuning

### CNN Model

Modify `train_cnn.py` to adjust:

```python
IMG_SIZE = (64, 64)        # Image resolution
BATCH_SIZE = 32            # Batch size
EPOCHS = 15                # Maximum epochs
LEARNING_RATE = 1e-3       # Adam optimizer learning rate

# Augmentation parameters
layers.RandomRotation(0.2)      # Rotation angle
layers.RandomZoom(0.15)         # Zoom range
layers.RandomBrightness(0.3)    # Brightness change
layers.RandomContrast(0.3)      # Contrast change
```

### AdaBoost Model

Modify `adaboost.ipynb` to adjust:

```python
from sklearn.ensemble import AdaBoostClassifier

ada_model = AdaBoostClassifier(
    n_estimators=50,        # Number of boosting rounds
    learning_rate=1.0,      # Learning rate
    random_state=42
)
```

## Performance Optimization

### For CNN Training

1. **Use GPU**: Install CUDA and cuDNN for 5-10x speedup
2. **Reduce image size**: Use 32×32 instead of 64×64 for faster training
3. **Increase batch size**: Use 64 or 128 for better GPU utilization
4. **Mixed precision**: Use `tf.keras.mixed_precision` for faster training

### For AdaBoost Training

1. **Feature selection**: Remove less important features
2. **Reduce dataset size**: Use stratified sampling for faster iteration
3. **Parallel processing**: Use `n_jobs=-1` in scikit-learn

## Troubleshooting

### CNN Training Issues

**Issue:** Out of memory error
```
ResourceExhaustedError: OOM when allocating tensor
```
**Solution:** Reduce batch size or image size

**Issue:** Model not converging
```
Validation accuracy not improving
```
**Solution:** Reduce learning rate or increase augmentation

**Issue:** Slow training on CPU
```
Training takes too long
```
**Solution:** Use GPU or reduce dataset size

### AdaBoost Training Issues

**Issue:** Model overfitting
```
Training accuracy >> Validation accuracy
```
**Solution:** Reduce n_estimators or increase learning_rate

**Issue:** Class imbalance
```
Model biased towards majority class
```
**Solution:** Use `class_weight='balanced'` in AdaBoost

## Model Versioning

Keep track of model versions:

```
models/
├── plant_cnn_model_v1.keras      # Initial model
├── plant_cnn_model_v2.keras      # After augmentation tuning
├── plant_cnn_model_v3.keras      # After hyperparameter tuning
└── plant_cnn_model.keras         # Current production model
```

## Continuous Improvement

1. **Collect user feedback** on predictions
2. **Identify misclassified samples**
3. **Add new training data** for problematic classes
4. **Retrain models** periodically
5. **A/B test** new models before deployment

## References

- [TensorFlow Documentation](https://www.tensorflow.org/api_docs)
- [scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [PlantVillage Dataset Paper](https://arxiv.org/abs/1604.04004)
- [SHAP Documentation](https://shap.readthedocs.io/)

---

**Last Updated:** April 30, 2026
