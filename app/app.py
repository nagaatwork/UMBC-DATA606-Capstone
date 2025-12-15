import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ----- LOAD TRAINED PIPELINE MODEL AND THRESHOLD -----
model = joblib.load("stacking_model_pipeline.pkl")
best_f1_threshold = float(np.load("model_threshold.npy")[0])

# ----- PAGE CONFIG & STYLING -----
st.set_page_config(page_title="Readmission Predictor", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 10px;
    }
    .risk-high {
        background-color: #ffcccc;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff0000;
    }
    .risk-low {
        background-color: #ccffcc;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #00cc00;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Patient Readmission Risk Prediction")
st.write("Enter key patient information to predict 30-day readmission risk.")

# ----- TABS FOR SINGLE VS BATCH PREDICTION -----
tab1, tab2 = st.tabs(["Single Patient", "Batch Upload (CSV)"])

# All required columns for the model
required_columns = [
    'encounter_id', 'patient_nbr', 'race', 'gender', 'age', 'weight',
    'admission_type_desc', 'time_in_hospital', 'payer_code', 'medical_specialty',
    'num_lab_procedures', 'num_procedures', 'number_outpatient', 'number_emergency',
    'number_inpatient', 'diag_1', 'diag_2', 'diag_3', 'number_diagnoses',
    'max_glu_serum', 'A1Cresult', 'metformin', 'repaglinide', 'nateglinide',
    'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide', 'glyburide',
    'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol',
    'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin',
    'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone',
    'metformin-rosiglitazone', 'metformin-pioglitazone', 'change', 'diabetesMed',
    'age_group', 'num_medications', 'many_meds', 'high_utilization', 'adm_type_grouped',
    'glucose_result', 'hba1c_result', 'diabetes_type', 'diabetes_complication', 'insulin_status'
]

# Minimal/neutral defaults for non-displayed features
defaults = {
    'encounter_id': 0,
    'patient_nbr': 0,
    'race': 'Caucasian',
    'gender': 'Female',
    'weight': '?',
    'payer_code': '?',
    'medical_specialty': '?',
    'num_lab_procedures': 45,
    'num_procedures': 1,
    'max_glu_serum': 'None',
    'metformin': 'No',
    'repaglinide': 'No',
    'nateglinide': 'No',
    'chlorpropamide': 'No',
    'glimepiride': 'No',
    'acetohexamide': 'No',
    'glipizide': 'No',
    'glyburide': 'No',
    'tolbutamide': 'No',
    'pioglitazone': 'No',
    'rosiglitazone': 'No',
    'acarbose': 'No',
    'miglitol': 'No',
    'troglitazone': 'No',
    'tolazamide': 'No',
    'examide': 'No',
    'citoglipton': 'No',
    'glyburide-metformin': 'No',
    'glipizide-metformin': 'No',
    'glimepiride-pioglitazone': 'No',
    'metformin-rosiglitazone': 'No',
    'metformin-pioglitazone': 'No',
}

category_levels = {
    "adm_type_grouped": ['Discharged to home', 'Physician Referral', 'Other'],
    "diabetes_type": ['Type 1', 'Type 2', 'Gestational', 'Other'],
    "insulin_status": ['No', 'Steady', 'Up', 'Down']
}

def prepare_features(features_dict):
    """Fill missing columns with neutral defaults"""
    for col in required_columns:
        if col not in features_dict:
            features_dict[col] = defaults.get(col, np.nan)
    
    X_input = pd.DataFrame([features_dict])
    for col, levels in category_levels.items():
        if col in X_input.columns:
            X_input[col] = pd.Categorical(X_input[col], categories=levels)
    return X_input

# ========== TAB 1: SINGLE PATIENT - HIGH IMPACT FEATURES ONLY ==========
with tab1:
    st.subheader("Enter Patient Information")
    
    features = {}
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Demographics & History**")
        features['age_group'] = st.number_input("Age (years)", min_value=0, max_value=120, value=65, 
                                                help="Older patients have higher readmission risk")
        features['age'] = f"[{(features['age_group']//10)*10}-{((features['age_group']//10)*10)+10})"
        
        features['number_inpatient'] = st.number_input("Prior Inpatient Visits (past year)", 
                                                       min_value=0, max_value=20, value=0,
                                                       help="Previous hospitalizations strongly predict readmission")
        
        features['number_emergency'] = st.number_input("Emergency Visits (past year)", 
                                                       min_value=0, max_value=20, value=0,
                                                       help="Recent ER visits indicate instability")
        
        features['number_outpatient'] = st.number_input("Outpatient Visits (past year)", 
                                                        min_value=0, max_value=20, value=0)
    
    with col2:
        st.markdown("**Current Hospitalization**")
        features['time_in_hospital'] = st.number_input("Length of Stay (days)", 
                                                       min_value=1, max_value=14, value=3,
                                                       help="Longer stays may indicate complications")
        
        features['num_medications'] = st.number_input("Number of Medications", 
                                                      min_value=0, max_value=50, value=10,
                                                      help="High medication burden increases risk")
        features['many_meds'] = 1 if features['num_medications'] > 20 else 0
        
        features['number_diagnoses'] = st.number_input("Number of Diagnoses", 
                                                       min_value=1, max_value=16, value=7,
                                                       help="Multiple comorbidities increase complexity")
        
        features['admission_type_desc'] = st.selectbox("Admission Type",
            ['Emergency', 'Urgent', 'Elective', 'Newborn', 'Not Available'],
            help="Emergency admissions have higher readmission rates")
        
        # Map admission type to grouped version
        adm_map = {
            'Emergency': 'Other',
            'Urgent': 'Other',
            'Elective': 'Physician Referral',
            'Newborn': 'Other',
            'Not Available': 'Other'
        }
        features['adm_type_grouped'] = adm_map.get(features['admission_type_desc'], 'Other')
        
        features['high_utilization'] = 1 if (features['number_inpatient'] + features['number_emergency']) > 4 else 0
    
    with col3:
        st.markdown("**Diabetes Management**")
        features['hba1c_result'] = st.number_input('Most Recent HbA1c (%)', 
                                                   min_value=3.0, max_value=15.0, value=7.0,
                                                   help="HbA1c >8% indicates poor glucose control")
        # Map to categorical
        if features['hba1c_result'] > 8:
            features['A1Cresult'] = '>8'
        elif features['hba1c_result'] > 7:
            features['A1Cresult'] = '>7'
        else:
            features['A1Cresult'] = 'Norm'
        
        features['glucose_result'] = st.number_input('Most Recent Glucose (mg/dL)', 
                                                     min_value=20, max_value=600, value=110)
        
        features['diabetes_type'] = st.selectbox("Diabetes Type", 
                                                 ['Type 1', 'Type 2', 'Gestational', 'Other'])
        
        features['diabetes_complication'] = st.selectbox("Has Diabetes Complications?", 
                                                         [0, 1], format_func=lambda x: 'Yes' if x else 'No',
                                                         help="Complications indicate disease severity")
        
        features['insulin_status'] = st.selectbox("Insulin Management", 
                                                  ['No', 'Steady', 'Up', 'Down'],
                                                  help="Insulin changes suggest unstable control")
        features['insulin'] = features['insulin_status']
        
        features['change'] = st.selectbox("Medication Changed?", 
                                         ['No', 'Ch'], format_func=lambda x: 'Yes' if x == 'Ch' else 'No',
                                         help="Medication changes may indicate problems")
        
        features['diabetesMed'] = st.selectbox("On Diabetes Medication?", 
                                              ['Yes', 'No'])
        
        features['diag_1'] = st.text_input("Primary Diagnosis (ICD-9)", value='250',
                                          help="Primary diagnosis code (e.g., 250 for diabetes)")
        features['diag_2'] = st.text_input("Secondary Diagnosis (ICD-9)", value='250')
        features['diag_3'] = st.text_input("Tertiary Diagnosis (ICD-9)", value='250')
    
    if st.button("Predict Readmission Risk"):
        X_input = prepare_features(features)
        
        try:
            y_proba = model.predict_proba(X_input)[0, 1]
            will_readmit = y_proba >= best_f1_threshold
            
            if will_readmit:
                st.markdown(f'<div class="risk-high"><h2>HIGH RISK - Patient will likely be READMITTED</h2>'
                           f'<p style="font-size:20px;">Risk Probability: <b>{y_proba:.1%}</b></p>'
                           f'<p>Threshold: {best_f1_threshold:.2f}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="risk-low"><h2>LOW RISK - Patient will likely NOT be readmitted</h2>'
                           f'<p style="font-size:20px;">Risk Probability: <b>{y_proba:.1%}</b></p>'
                           f'<p>Threshold: {best_f1_threshold:.2f}</p></div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction error: {e}")

# ========== TAB 2: BATCH UPLOAD ==========
with tab2:
    st.subheader("Upload CSV File for Batch Predictions")
    st.write("Upload a CSV with patient records.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} patient records")
        st.dataframe(df.head())
        
        if st.button("Predict for All Patients"):
            try:
                # Fill missing columns
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = defaults.get(col, np.nan)
                
                # Set categorical types
                for col, levels in category_levels.items():
                    if col in df.columns:
                        df[col] = pd.Categorical(df[col], categories=levels)
                
                probabilities = model.predict_proba(df[required_columns])[:, 1]
                predictions = (probabilities >= best_f1_threshold).astype(int)
                
                df['risk_probability'] = probabilities
                df['will_readmit'] = predictions
                df['prediction'] = df['will_readmit'].map({1: 'WILL READMIT', 0: 'Will NOT readmit'})
                
                st.success("Predictions complete!")
                st.dataframe(df[['risk_probability', 'prediction']])
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name='readmission_predictions.csv',
                    mime='text/csv',
                )
            except Exception as e:
                st.error(f"Error: {e}")
