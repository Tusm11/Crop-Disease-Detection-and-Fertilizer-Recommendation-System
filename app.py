import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import joblib
import json
import os
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from soil_lookup import get_soil_crop_values, get_available_soil_types
from sklearn.preprocessing import StandardScaler

<<<<<<< HEAD
st.set_page_config(page_title="Crop Disease Detection and Fertilizer Detection", page_icon="🌿", layout="centered")

# Load models
=======
st.set_page_config(page_title="Crop Disease Detection and Fertilizer Detection", page_icon="🌿")

#Load models
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
@st.cache_resource
def load_assets():
    cnn, ada, le_soil, le_crop, le_fert, class_names, scaler = None, None, None, None, None, None, None

<<<<<<< HEAD
    if os.path.exists('models/plant_cnn_model.h5'):
        cnn = tf.keras.models.load_model('models/plant_cnn_model.h5')
    elif os.path.exists('models/plant_cnn_model.keras'):
=======
    if os.path.exists('models/plant_cnn_model.keras'):
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
        cnn = tf.keras.models.load_model('models/plant_cnn_model.keras')

    if os.path.exists('models/fertilizer_ada_model.pkl'):
        ada = joblib.load('models/fertilizer_ada_model.pkl')
        le_soil = joblib.load('models/le_soil.pkl')
        le_crop = joblib.load('models/le_crop.pkl')
        le_fert = joblib.load('models/le_fert.pkl')
<<<<<<< HEAD

    # Load or create scaler
    if os.path.exists('models/scaler.pkl'):
        scaler = joblib.load('models/scaler.pkl')
    else:
        # Create scaler if not saved (fallback)
        import pandas as pd
        if os.path.exists('fertilizer_recommendation.csv'):
            df = pd.read_csv('fertilizer_recommendation.csv')
            numeric_features = ['Nitrogen_Level', 'Phosphorus_Level', 'Potassium_Level', 'Temperature', 'Humidity', 'Soil_Moisture']
=======
        
        # Load or create scaler
        if os.path.exists('models/scaler.pkl'):
            scaler = joblib.load('models/scaler.pkl')
        else:
            # Create scaler if not saved (fallback)
            import pandas as pd
            df = pd.read_csv('fertilizer_recommendation.csv')
            numeric_features = ['Nitrogen_Level', 'Phosphorus_Level', 'Potassium_Level', 
                               'Temperature', 'Humidity', 'Soil_Moisture']
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
            scaler = StandardScaler()
            scaler.fit(df[numeric_features])

    if os.path.exists('models/class_names.json'):
        with open('models/class_names.json') as f:
            class_names = json.load(f)

    return cnn, ada, le_soil, le_crop, le_fert, class_names, scaler

cnn_model, ada_model, le_soil, le_crop, le_fert, class_names, scaler = load_assets()

@st.cache_resource
def get_shap_explainer(_ada):
<<<<<<< HEAD
    if _ada is None: return None
    import pandas as pd
    if os.path.exists('fertilizer_recommendation.csv'):
        df = pd.read_csv('fertilizer_recommendation.csv')
        background = df.sample(n=min(100, len(df)), random_state=42)
        numeric_features = ['Nitrogen_Level', 'Phosphorus_Level', 'Potassium_Level', 'Temperature', 'Humidity', 'Soil_Moisture']
        from sklearn.preprocessing import LabelEncoder
        le_soil_temp = LabelEncoder()
        le_crop_temp = LabelEncoder()
        background['Soil_Type_enc'] = le_soil_temp.fit_transform(background['Soil_Type'])
        background['Crop_Type_enc'] = le_crop_temp.fit_transform(background['Crop_Type'])
        from sklearn.preprocessing import StandardScaler
        sc_temp = StandardScaler()
        background[numeric_features] = sc_temp.fit_transform(background[numeric_features])
        X_background = background[numeric_features + ['Soil_Type_enc', 'Crop_Type_enc']].values
        return shap.KernelExplainer(_ada.predict_proba, X_background)
    return None

shap_explainer = get_shap_explainer(ada_model)

=======
    # AdaBoost is not supported by TreeExplainer, use KernelExplainer instead
    if _ada is None:
        return None
    
    # Create a small background dataset for KernelExplainer
    import pandas as pd
    df = pd.read_csv('fertilizer_recommendation.csv')
    
    # Sample 100 random rows for background
    background = df.sample(n=min(100, len(df)), random_state=42)
    
    # Prepare features
    numeric_features = ['Nitrogen_Level', 'Phosphorus_Level', 'Potassium_Level', 
                       'Temperature', 'Humidity', 'Soil_Moisture']
    
    # Encode categorical
    from sklearn.preprocessing import LabelEncoder
    le_soil_temp = LabelEncoder()
    le_crop_temp = LabelEncoder()
    
    background['Soil_Type_enc'] = le_soil_temp.fit_transform(background['Soil_Type'])
    background['Crop_Type_enc'] = le_crop_temp.fit_transform(background['Crop_Type'])
    
    # Scale numeric features
    from sklearn.preprocessing import StandardScaler
    sc_temp = StandardScaler()
    background[numeric_features] = sc_temp.fit_transform(background[numeric_features])
    
    # Prepare background data
    X_background = background[numeric_features + ['Soil_Type_enc', 'Crop_Type_enc']].values
    
    # Use KernelExplainer (slower but works with any model)
    return shap.KernelExplainer(_ada.predict_proba, X_background)

shap_explainer = get_shap_explainer(ada_model)

# Map CNN class name → disease type label (blight, rust, mildew, etc.)
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
def parse_disease(class_name):
    """Returns (crop, disease_type, is_healthy)"""
    if '___' in class_name:
        parts = class_name.split('___')
<<<<<<< HEAD
        crop = parts[0].replace('_', ' ').replace(',', '').strip()
        label = parts[1].replace('_', ' ').strip()
    else:
        crop = class_name.replace('_', ' ').strip()
        label = crop

    is_healthy = 'healthy' in label.lower()
=======
        crop  = parts[0].replace('_', ' ').replace(',', '').strip()
        label = parts[1].replace('_', ' ').strip()
    else:
        crop  = class_name.replace('_', ' ').strip()
        label = crop

    is_healthy = 'healthy' in label.lower()

    # Normalise disease type to a short category
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
    label_lower = label.lower()
    if is_healthy:
        disease_type = 'Healthy'
    elif any(x in label_lower for x in ['blight', 'spot', 'scorch']):
        disease_type = 'Blight / Leaf Spot'
    elif 'rust' in label_lower:
        disease_type = 'Rust'
    elif 'mildew' in label_lower:
        disease_type = 'Powdery Mildew'
    elif any(x in label_lower for x in ['rot', 'measles']):
        disease_type = 'Rot'
    elif any(x in label_lower for x in ['virus', 'curl', 'mosaic']):
        disease_type = 'Viral Disease'
    elif any(x in label_lower for x in ['mite', 'hopper', 'pest']):
        disease_type = 'Pest Damage'
    elif any(x in label_lower for x in ['bacterial', 'greening']):
        disease_type = 'Bacterial Disease'
    else:
        disease_type = label.title()
<<<<<<< HEAD
    return crop, disease_type, is_healthy

CROP_MAP = {
    'Corn': 'Maize', 'Pepperbell': 'Potato', 'Squash': 'Maize',
=======

    return crop, disease_type, is_healthy

# Map CNN crop name → AdaBoost crop label
CROP_MAP = {
    'Corn': 'Maize', 'Pepper bell': 'Potato', 'Squash': 'Maize',
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
    'Soybean': 'Sugarcane', 'Apple': 'Tomato', 'Grape': 'Tomato',
    'Orange': 'Tomato', 'Peach': 'Tomato', 'Cherry': 'Tomato',
    'Strawberry': 'Tomato', 'Blueberry': 'Tomato', 'Raspberry': 'Tomato'
}

def get_ada_crop(cnn_crop):
<<<<<<< HEAD
    return CROP_MAP.get(cnn_crop, cnn_crop)

def predict_fertilizer(crop, soil='Loamy'):
    soil_values = get_soil_crop_values(soil, crop)
=======
    """Map CNN crop to AdaBoost crop (only 7 crops in fertilizer dataset)"""
    # AdaBoost knows: Cotton, Maize, Wheat, Potato, Rice, Sugarcane, Tomato
    return CROP_MAP.get(cnn_crop, cnn_crop)

def predict_fertilizer(crop, soil='Loamy'):
    """
    Predict fertilizer based on crop and soil type.
    Samples actual values from dataset for that soil+crop combination.
    """
    # Get soil+crop based values (sampled from actual data, not averaged)
    soil_values = get_soil_crop_values(soil, crop)
    
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
    try:
        soil_enc = le_soil.transform([soil])[0]
    except:
        soil_enc = 0
<<<<<<< HEAD
    try:
        crop_enc = le_crop.transform([crop])[0]
    except:
=======
    
    try:
        crop_enc = le_crop.transform([crop])[0]
    except:
        # Fallback to Maize if crop not in encoder
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
        try:
            crop_enc = le_crop.transform(['Maize'])[0]
            crop = 'Maize'
        except:
            crop_enc = 0
<<<<<<< HEAD
    numeric_vals = [soil_values['N'], soil_values['P'], soil_values['K'], 
                    soil_values['Temperature'], soil_values['Humidity'], soil_values['Soil_Moisture']]
    numeric_scaled = scaler.transform([numeric_vals])[0]
    X = np.array([[*numeric_scaled, soil_enc, crop_enc]])
    
    # Use DataFrame for prediction to avoid sklearn feature name warnings
    import pandas as pd
    train_feature_names = ['Nitrogen_Level', 'Phosphorus_Level', 'Potassium_Level', 
                          'Temperature', 'Humidity', 'Soil_Moisture', 'Soil_Type', 'Crop_Type']
    X_df = pd.DataFrame(X, columns=train_feature_names)
    
    feature_names = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Soil Moisture', 'Soil Type', 'Crop Type']
    pred_idx = ada_model.predict(X_df)[0]
    fert_name = le_fert.inverse_transform([pred_idx])[0]
    
    if shap_explainer:
        shap_vals = shap_explainer.shap_values(X_df)
        if isinstance(shap_vals, np.ndarray) and shap_vals.ndim == 3:
            sv = shap_vals[0, :, pred_idx]
=======

    # Feature order MUST match training: 
    # Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Soil_Moisture, Soil_Type, Crop_Type
    numeric_vals = [
        soil_values['N'], 
        soil_values['P'], 
        soil_values['K'],
        soil_values['Temperature'],
        soil_values['Humidity'],
        soil_values['Soil_Moisture']
    ]
    
    # Apply StandardScaler to numeric features
    numeric_scaled = scaler.transform([numeric_vals])[0]
    
    # Combine scaled numeric + encoded categorical
    # Order: [N_scaled, P_scaled, K_scaled, T_scaled, H_scaled, M_scaled, Soil_enc, Crop_enc]
    X = np.array([[*numeric_scaled, soil_enc, crop_enc]])
    
    feature_names = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature',
                     'Humidity', 'Soil Moisture', 'Soil Type', 'Crop Type']

    pred_idx = ada_model.predict(X)[0]
    fert_name = le_fert.inverse_transform([pred_idx])[0]
    
    # Debug: Print what's being predicted
    print(f"DEBUG: Crop={crop}, Soil={soil}")
    print(f"DEBUG: Numeric values (unscaled): {numeric_vals}")
    print(f"DEBUG: Numeric values (scaled): {numeric_scaled}")
    print(f"DEBUG: Soil_enc={soil_enc}, Crop_enc={crop_enc}")
    print(f"DEBUG: Predicted fertilizer: {fert_name}")

    # SHAP - KernelExplainer returns different format
    if shap_explainer:
        shap_vals = shap_explainer.shap_values(X)
        
        # KernelExplainer returns array of shape (n_samples, n_features, n_classes)
        # We want SHAP values for the predicted class
        if isinstance(shap_vals, np.ndarray) and shap_vals.ndim == 3:
            sv = shap_vals[0, :, pred_idx]  # Get SHAP values for predicted class
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
        elif isinstance(shap_vals, list):
            sv = shap_vals[pred_idx][0]
        else:
            sv = shap_vals[0]
    else:
        sv = np.zeros(len(feature_names))
<<<<<<< HEAD
    sv = np.array(sv).flatten()
    if len(sv) != len(feature_names):
        sv = np.pad(sv, (0, max(0, len(feature_names) - len(sv))), mode='constant')[:len(feature_names)]
    display_vals = [*numeric_vals, soil_enc, crop_enc]
    return fert_name, sv, feature_names, display_vals

# UI
=======
    
    # Ensure 1D array and correct length
    sv = np.array(sv).flatten()
    if len(sv) != len(feature_names):
        sv = np.pad(sv, (0, max(0, len(feature_names) - len(sv))), mode='constant')[:len(feature_names)]

    # Return original (unscaled) values for display
    display_vals = [*numeric_vals, soil_enc, crop_enc]
    return fert_name, sv, feature_names, display_vals

#UI
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
st.title("Crop Disease Detection and Fertilizer Detection")
st.caption("Upload a leaf → CNN detects crop → AdaBoost recommends fertilizer")
st.divider()

uploaded_file = st.file_uploader("Upload leaf image", type=["jpg", "jpeg", "png"])

<<<<<<< HEAD
if uploaded_file and st.session_state.get('last_file_name') != uploaded_file.name:
    if 'cnn_results' in st.session_state: del st.session_state.cnn_results
    st.session_state.last_file_name = uploaded_file.name
elif not uploaded_file and st.session_state.get('last_file_name') is not None:
    if 'cnn_results' in st.session_state: del st.session_state.cnn_results
    st.session_state.last_file_name = None

if uploaded_file:
    st.image(uploaded_file, width=400)

if 'cnn_results' in st.session_state:
    results = st.session_state.cnn_results
    st.divider()
    col_diag, col_fert = st.columns(2)
    with col_diag:
        st.subheader("🔬 Disease Diagnosis")
        if results['is_healthy']:
            st.success("✅ **Healthy Leaf**")
        else:
            st.error("⚠️ **Diseased Leaf**")
            st.caption(f"Disease Type: {results['disease_type']}")

=======
# Clear previous results if a new file is uploaded or if file is removed
if uploaded_file and st.session_state.get('last_file_name') != uploaded_file.name:
    if 'cnn_results' in st.session_state:
        del st.session_state.cnn_results
    st.session_state.last_file_name = uploaded_file.name
elif not uploaded_file and st.session_state.get('last_file_name') is not None:
    # File was removed - clear results
    if 'cnn_results' in st.session_state:
        del st.session_state.cnn_results
    st.session_state.last_file_name = None

if uploaded_file:
    st.image(uploaded_file, use_column_width=True)

# Show analysis results if available
if 'cnn_results' in st.session_state:
    results = st.session_state.cnn_results
    
    st.divider()
    col_diag, col_fert = st.columns(2)
    
    with col_diag:
        st.subheader("🔬Disease Diagnosis")
        
        if results['is_healthy']:
            st.success(f"✅ **Healthy Leaf**")
        else:
            st.error(f"⚠️ **Diseased Leaf**")
            # Show disease type in smaller text
            st.caption(f"Disease Type: {results['disease_type']}")
        
        # Gradient heatmap (cached in session state)
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
        if 'feature_map' not in st.session_state.cnn_results:
            img_tensor = tf.convert_to_tensor(np.expand_dims(results['img_arr'], 0))
            with tf.GradientTape() as tape:
                tape.watch(img_tensor)
<<<<<<< HEAD
                out = cnn_model(img_tensor)
                loss = out[:, results['class_idx']]
            grads = tape.gradient(loss, img_tensor)[0].numpy()
=======
                out  = cnn_model(img_tensor)
                loss = out[:, results['class_idx']]
            grads      = tape.gradient(loss, img_tensor)[0].numpy()
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
            impact_map = np.max(np.abs(grads), axis=-1)
            st.session_state.cnn_results['feature_map'] = impact_map
        else:
            impact_map = st.session_state.cnn_results['feature_map']
<<<<<<< HEAD
        fig, ax = plt.subplots(figsize=(3, 3))
        sns.heatmap(impact_map, ax=ax, cmap="YlOrRd", cbar=False, xticklabels=False, yticklabels=False)
        ax.set_title("Feature Impact Map")
        st.pyplot(fig)

    with col_fert:
        st.subheader("🌱 Fertilizer Recommendation")
        available_soils = get_available_soil_types()
        soil_type = st.selectbox("Soil Type", available_soils, key='soil_select')
        if ada_model and shap_explainer:
            fert_name, sv, feat_names, x_vals = predict_fertilizer(results['ada_crop'], soil=soil_type)
            st.success(f"Recommended: **{fert_name}**")
=======
        
        fig, ax = plt.subplots(figsize=(3, 3))
        sns.heatmap(impact_map, ax=ax, cmap="YlOrRd",
                    cbar=False, xticklabels=False, yticklabels=False)
        ax.set_title("Feature Impact Map")
        st.pyplot(fig)
    
    with col_fert:
        st.subheader("🌱 Fertilizer Recommendation")
        
        # Only ask for soil type - no location needed
        available_soils = get_available_soil_types()
        soil_type = st.selectbox("Soil Type", available_soils, key='soil_select')
        
        if ada_model and shap_explainer:
            fert_name, sv, feat_names, x_vals = predict_fertilizer(
                results['ada_crop'], soil=soil_type
            )
            st.success(f"Recommended: **{fert_name}**")
            
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
            st.markdown("**Why this fertilizer?**")
            top_feat_idx = np.argsort(np.abs(sv))[::-1][:3]
            for idx in top_feat_idx:
                if idx < len(sv) and idx < len(x_vals):
                    direction = "⬆️" if sv[idx] > 0 else "⬇️"
                    st.write(f"{direction} **{feat_names[idx]}** = `{x_vals[idx]:.1f}` (SHAP: `{sv[idx]:+.3f}`)")
<<<<<<< HEAD
            st.markdown("**📊 SHAP Feature Importance**")
            sorted_i = np.argsort(sv)
            colors = ['#e74c3c' if sv[i] > 0 else '#3498db' for i in sorted_i]
=======
            
            st.markdown("**📊 SHAP Feature Importance**")
            sorted_i = np.argsort(sv)
            colors   = ['#e74c3c' if sv[i] > 0 else '#3498db' for i in sorted_i]
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
            fig2, ax2 = plt.subplots(figsize=(5, 4))
            ax2.barh([feat_names[i] for i in sorted_i], [sv[i] for i in sorted_i], color=colors)
            ax2.axvline(0, color='black', linewidth=0.8)
            ax2.set_xlabel("SHAP Value")
            ax2.set_title(f"Why '{fert_name}'?")
            plt.tight_layout()
            st.pyplot(fig2)
<<<<<<< HEAD

=======
    
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
    st.divider()
    if results['is_healthy']:
        st.success(f"✅ Leaf is healthy. Apply **{fert_name}** for continued growth.")
    else:
        st.warning(f"⚠️ Leaf is diseased. Apply **{fert_name}** to support recovery.")

<<<<<<< HEAD
=======
# Show button and message only if no results yet
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
if 'cnn_results' not in st.session_state:
    if st.button("Analyse"):
        if not uploaded_file:
            st.warning("Please upload a leaf image first.")
        elif cnn_model is None or class_names is None:
            st.error("CNN model not found.")
        else:
<<<<<<< HEAD
            img = Image.open(uploaded_file).convert("RGB").resize((64, 64))
            img_arr = np.array(img).astype('float32')
            white_mask = np.all(img_arr > 250, axis=-1)
            img_arr[white_mask] = [128, 128, 128]
            augmented = [img_arr]
            for angle in [5, -5]:
                augmented.append(tf.keras.preprocessing.image.apply_affine_transform(img_arr, theta=angle, row_axis=0, col_axis=1, channel_axis=2))
            for delta in [20, -20]:
                augmented.append(np.clip(img_arr + delta, 0.0, 255.0))
            augmented.append(np.fliplr(img_arr).copy())
=======
            # Run CNN prediction and store in session state
            img = Image.open(uploaded_file).convert("RGB").resize((64, 64))
            img_arr = np.array(img).astype('float32')
            
            # Only replacing pure white background (RGB > 250), not light leaf areas
            white_mask = np.all(img_arr > 250, axis=-1)
            img_arr[white_mask] = [128, 128, 128]
            
            augmented = [img_arr]
            for angle in [5, -5]:
                augmented.append(tf.keras.preprocessing.image.apply_affine_transform(
                    img_arr, theta=angle, row_axis=0, col_axis=1, channel_axis=2))
            for delta in [20, -20]:
                augmented.append(np.clip(img_arr + delta, 0.0, 255.0))
            augmented.append(np.fliplr(img_arr).copy())
            
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
            all_preds = [cnn_model.predict(np.expand_dims(a, 0), verbose=0) for a in augmented]
            avg_preds = np.mean(all_preds, axis=0)[0]
            class_idx = int(np.argmax(avg_preds))
            accuracy = float(avg_preds[class_idx])
<<<<<<< HEAD
            raw_class_name = class_names[class_idx]
            crop, disease_type, is_healthy = parse_disease(raw_class_name)
            ada_crop = get_ada_crop(crop)
            st.session_state.cnn_results = {
                'crop': crop, 'disease_type': disease_type, 'is_healthy': is_healthy, 'ada_crop': ada_crop,
                'accuracy': accuracy, 'raw_class_name': raw_class_name, 'img_arr': img_arr, 'class_idx': class_idx
            }
            st.rerun()
    st.info("Upload a leaf image and click Analyse.")
=======
            
            raw_class_name = class_names[class_idx]
            crop, disease_type, is_healthy = parse_disease(raw_class_name)
            ada_crop = get_ada_crop(crop)
            
            st.session_state.cnn_results = {
                'crop': crop, 'disease_type': disease_type, 'is_healthy': is_healthy,
                'ada_crop': ada_crop, 'accuracy': accuracy, 'raw_class_name': raw_class_name,
                'img_arr': img_arr, 'class_idx': class_idx
            }
            st.rerun()
    
    st.info("Upload a leaf image and click Analyse.")
>>>>>>> ac3b109be22706103aa5be7f8e3163333838ef4b
