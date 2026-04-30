# Crop Disease Detection and Fertilizer Recommendation System

A machine learning-based web application that detects crop diseases from leaf images and recommends appropriate fertilizers based on soil and crop conditions.

## Project Overview

This is a **Problem-Based Learning (PBL)** project that combines:
- **CNN (Convolutional Neural Network)** for crop disease detection
- **AdaBoost Classifier** for fertilizer recommendations
- **SHAP (SHapley Additive exPlanations)** for model interpretability

## Features

✅ **Disease Detection**: Upload a leaf image to detect diseases across 59 crop-disease classes
✅ **Fertilizer Recommendation**: Get personalized fertilizer suggestions based on soil type and crop
✅ **Model Explainability**: SHAP visualizations show why specific fertilizers are recommended
✅ **Feature Impact Maps**: Gradient-based heatmaps highlight disease indicators in leaf images
✅ **Multi-crop Support**: Handles multiple crop types (Tomato, Potato, Corn, etc.)

## Project Structure

```
ML PBL - 23R11A66P3/
├── app.py                              # Main Streamlit application
├── train_cnn.py                        # CNN model training script
├── adaboost.ipynb                      # AdaBoost model training notebook
├── soil_lookup.py                      # Soil-crop value lookup utility
├── requirements.txt                    # Python dependencies
├── runtime.txt                         # Python version specification
├── .streamlit/config.toml              # Streamlit configuration
├── models/
│   ├── plant_cnn_model.keras          # Trained CNN model (inference)
│   ├── plant_cnn_model.h5             # Trained CNN model (backup)
│   ├── fertilizer_ada_model.pkl       # Trained AdaBoost model
│   ├── class_names.json               # Disease class labels
│   ├── scaler.pkl                     # Feature scaler for AdaBoost
│   ├── le_soil.pkl                    # Soil type encoder
│   ├── le_crop.pkl                    # Crop type encoder
│   └── le_fert.pkl                    # Fertilizer type encoder
├── fertilizer_recommendation.csv       # Fertilizer recommendation dataset
└── README.md                           # This file
```

## Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tusm11/Crop-Disease-Detection-and-Fertilizer-Recommendation-System.git
   cd "ML PBL - 23R11A66P3"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

### Deployment on Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" → Select your repository
4. Set main file path to `ML PBL - 23R11A66P3/app.py`
5. Deploy!

## Model Training

### CNN Model Training

The CNN model is trained on plant leaf disease images with data augmentation for robustness to varying light conditions.

**To retrain the CNN model:**

```bash
python train_cnn.py
```

**Training parameters:**
- Image size: 64×64 pixels
- Batch size: 32
- Epochs: 15 (with early stopping)
- Augmentation: Random flip, rotation, zoom, brightness, contrast
- Optimizer: Adam (learning rate: 0.001)
- Loss: Sparse categorical crossentropy

**Output:**
- `models/plant_cnn_model.keras` - Trained model
- `models/class_names.json` - Disease class labels
- `models/training_history.json` - Training metrics

### AdaBoost Model Training

The AdaBoost model recommends fertilizers based on soil properties, crop type, and environmental conditions.

**To retrain the AdaBoost model:**

Open and run `adaboost.ipynb` in Jupyter Notebook:

```bash
jupyter notebook adaboost.ipynb
```

**Features used:**
- Nitrogen, Phosphorus, Potassium levels
- Temperature, Humidity, Soil Moisture
- Soil Type (encoded)
- Crop Type (encoded)

**Output:**
- `models/fertilizer_ada_model.pkl` - Trained model
- `models/le_soil.pkl`, `le_crop.pkl`, `le_fert.pkl` - Label encoders
- `models/scaler.pkl` - Feature scaler

## Usage

### Web Application

1. **Upload a leaf image** (JPG, PNG, or JPEG)
2. **Click "Analyse"** to detect disease
3. **View results:**
   - Disease diagnosis with confidence score
   - Feature impact heatmap showing disease indicators
   - Recommended fertilizer based on soil type
   - SHAP explanation of why that fertilizer was recommended

### API Integration

The app can be extended to provide API endpoints for integration with other systems:

```python
# Example: Get disease prediction
image = load_image("leaf.jpg")
prediction = cnn_model.predict(image)
disease_class = class_names[np.argmax(prediction)]

# Example: Get fertilizer recommendation
fertilizer = predict_fertilizer(crop="Tomato", soil="Loamy")
```

## Dependencies

- **TensorFlow 2.15.1** - Deep learning framework
- **Streamlit 1.28.1** - Web app framework
- **scikit-learn 1.7.2** - Machine learning utilities
- **SHAP** - Model explainability
- **Pillow** - Image processing
- **OpenCV** - Computer vision
- **Pandas, NumPy** - Data manipulation
- **Matplotlib, Seaborn** - Visualization

See `requirements.txt` for complete list.

## Model Architecture

### CNN Model

```
Input (64×64×3)
    ↓
Rescaling (1/255)
    ↓
Block 1: Conv2D(32) → Conv2D(32) → MaxPool → Dropout(0.25)
    ↓
Block 2: Conv2D(64) → Conv2D(64) → MaxPool → Dropout(0.25)
    ↓
Block 3: Conv2D(128) → Conv2D(128) → MaxPool → Dropout(0.25)
    ↓
GlobalAveragePooling2D
    ↓
Dense(256, relu) → Dropout(0.5)
    ↓
Dense(128, relu) → Dropout(0.5)
    ↓
Dense(59, softmax) → Output (59 disease classes)
```

**Total Parameters:** 360,539 (1.38 MB)

### AdaBoost Model

- **Base Estimator:** Decision Tree Classifier
- **Number of Estimators:** 50
- **Learning Rate:** 1.0
- **Input Features:** 8 (6 numeric + 2 encoded categorical)
- **Output Classes:** 6 fertilizer types

## Performance Metrics

### CNN Model
- **Training Accuracy:** ~95%
- **Validation Accuracy:** ~92%
- **Best Epoch:** Early stopped at epoch 12

### AdaBoost Model
- **Training Accuracy:** ~88%
- **Cross-validation Score:** ~85%

## Troubleshooting

### Model Loading Issues

If you see "Could not load CNN model" error:

1. The app will automatically rebuild the model from scratch
2. It will try to load weights from the `.h5` backup file
3. If both fail, a fresh model is created (weights will be random)

### Streamlit Cloud Deployment Issues

**Issue:** Model deserialization error
**Solution:** The app includes automatic model rebuilding logic

**Issue:** Out of memory
**Solution:** Model is optimized for Streamlit Cloud's 1GB limit

## Future Enhancements

- [ ] Add more crop types and diseases
- [ ] Implement real-time camera feed support
- [ ] Add batch image processing
- [ ] Create mobile app version
- [ ] Add weather-based recommendations
- [ ] Implement user feedback loop for model improvement

## Team & Credits

**Project Type:** Problem-Based Learning (PBL)
**Institution:** [Your College Name]
**Year:** 2026

## License

This project is for educational purposes. Feel free to use and modify for learning.

## Contact & Support

For questions or issues, please open an issue on GitHub or contact the project maintainers.

---

*Streamlit cloud link*: https://crop-disease-detection-and-fertilizer-recommendation-system-rs.streamlit.app/

**GitHub Repository:** [Tusm11/Crop-Disease-Detection-and-Fertilizer-Recommendation-System](https://github.com/Tusm11/Crop-Disease-Detection-and-Fertilizer-Recommendation-System)
