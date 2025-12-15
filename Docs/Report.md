# Project Title: Predicting Hospital Readmissions

---

## Prepared for  
**UMBC Data Science Master's Capstone**  
Instructor: **Dr. Chaojie (Jay) Wang**

---

## Author  

**Naga Brahmendra Chowdary Devarapalli**

- **GitHub Repository:**  
  https://github.com/nagaatwork/UMBC-DATA606-Capstone

- **LinkedIn Profile:**  
  https://www.linkedin.com/in/your-linkedin-id

- **Final Presentation Slides:**  
  https://github.com/nagaatwork/UMBC-DATA606-Capstone/blob/main/Docs/Presentation3%20%5BAutosaved%5D.pptx

- **YouTube Demo / Presentation Video:**  
  <ADD YOUR YOUTUBE LINK HERE>

---

## Introduction

Hospital readmissions within 30 days are a widely used indicator of healthcare quality and efficiency. High readmission rates often reflect gaps in care coordination, premature discharge decisions, unmanaged chronic conditions, or inadequate post-discharge follow-up. In the United States, hospital readmissions also carry major financial consequences, as regulatory agencies such as Medicare and Medicaid impose penalties on hospitals with excessive readmission rates.

This project focuses on predicting the probability of hospital readmission within **30 days** for diabetic patients using the well-known **Diabetes 130-US hospitals (1999–2008)** dataset. The dataset contains over 100,000 hospital encounters across 130 U.S. hospitals and includes a rich combination of demographic, clinical, laboratory, medication, and utilization features.

By applying a structured machine learning pipeline — from exploratory data analysis to model deployment — this project aims to identify high-risk patients at the time of discharge and provide actionable insights that can support clinical decision-making.

---

## Why Does It Matter?

Reducing avoidable hospital readmissions is critical for improving patient outcomes and controlling healthcare costs.

From a **clinical perspective**, frequent readmissions may indicate:
- Poor discharge planning
- Inadequate patient education
- Lack of follow-up care
- Unmanaged comorbidities

From a **financial and policy perspective**, hospitals face:
- Reduced reimbursements
- Regulatory penalties
- Increased operational strain

Accurate readmission prediction models enable hospitals to:
- Identify high-risk patients early
- Allocate care coordination resources efficiently
- Schedule timely follow-ups
- Improve transitional care planning

Ultimately, predictive analytics can bridge the gap between raw clinical data and proactive, preventive healthcare delivery.

---

## Research Questions

This project seeks to answer the following questions:

1. **Can machine learning models effectively predict 30-day hospital readmission using encounter-level data?**

2. **Which features — demographic, clinical, laboratory, medication, or utilization-based — contribute most strongly to readmission risk?**

3. **How can a predictive model be operationalized into a practical, user-facing application for healthcare stakeholders?**

---

## Dataset Overview

### Data Source
- **UCI Machine Learning Repository**  
  Diabetes 130-US hospitals for years 1999–2008  
  https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008

### Dataset Characteristics
- **File:** `diabetic_data.csv`
- **Size:** ~18 MB
- **Shape:** 101,766 rows × 50 columns
- **Time Period:** 1999–2008
- **Unit of Analysis:** One hospital encounter per row
- **Data Type:** Fully de-identified patient records

---

## Target Variable

The original dataset includes a three-class variable `readmitted`:
- `NO`
- `>30`
- `<30`

For modeling purposes, this was transformed into a binary target:

- **`readmit_30d`**
  - `1` → Readmitted within 30 days (`<30`)
  - `0` → Not readmitted within 30 days (`NO` or `>30`)

### Target Distribution
- **Class 0 (Not readmitted): ~89%**
- **Class 1 (Readmitted within 30 days): ~11%**

This significant class imbalance strongly influenced modeling and evaluation decisions.

---

## Feature Overview

### Demographics
- `age`
- `gender`
- `race`

### Utilization & Encounter Characteristics
- `time_in_hospital`
- `number_outpatient`
- `number_emergency`
- `number_inpatient`
- `number_diagnoses`

### Clinical & Treatment Features
- `num_lab_procedures`
- `num_procedures`
- `num_medications`
- `A1Cresult`
- `max_glu_serum`
- Insulin usage indicators

### Admission & Discharge Information
- `admission_type_id`
- `admission_source_id`
- `discharge_disposition_id`
- Mapped descriptive admission types

---

## Exploratory Data Analysis (EDA)

### Data Quality Checks
- Replaced all `"?"` values with `NaN`
- Removed or ignored features with excessive missingness (e.g., `weight`, `payer_code`)
- Verified no exact duplicate encounters

### Key EDA Findings
- Readmitted patients had:
  - Longer hospital stays
  - Higher numbers of inpatient and emergency visits
  - Slightly higher medication counts
- Certain discharge dispositions (e.g., hospice, skilled nursing facilities) showed elevated readmission risk
- Laboratory indicators (`A1Cresult`, `max_glu_serum`) showed modest but meaningful associations

EDA confirmed that readmission risk is influenced by **both utilization history and clinical complexity**.

---

## Feature Engineering

Several domain-informed features were engineered:

- **Age Group Extraction**
  - Converted age brackets (e.g., `[60–70)`) into numeric midpoints

- **Medication Burden Flag**
  - `many_meds = 1` if `num_medications > 20`

- **High Utilization Indicator**
  - Combined outpatient, inpatient, and emergency visits

- **Grouped Admission Types**
  - Rare admission categories grouped as `"Other"`

These transformations improved model interpretability and robustness.

---

## Modeling Approach

### Train–Test Split
- **80% training / 20% testing**
- Stratified split to preserve class imbalance

### Preprocessing Pipeline
- Numeric features:
  - Mean imputation
  - Standard scaling
- Categorical features:
  - Mode imputation
  - One-hot encoding
- Implemented using `ColumnTransformer`

---

## Handling Class Imbalance

Multiple strategies were explored:
- **SMOTE oversampling**
- **Class-weighted models**
- **Threshold optimization**
- **Precision–Recall tradeoff analysis**

Evaluation emphasized **ROC-AUC, Recall, Precision, and F1-score**, rather than accuracy alone.

---

## Models Evaluated

- Logistic Regression (baseline)
- Random Forest
- XGBoost
- Stacking Ensemble (XGBoost + RF + Logistic Regression)

### Best Overall Performance
- **Stacking Classifier**
- ROC-AUC ≈ **0.70**
- Balanced recall for high-risk patients
- Strong generalization across folds

---

## Model Evaluation Strategy

- ROC curves
- Precision–Recall curves
- F1-optimized thresholds
- Confusion matrices
- Feature importance analysis (XGBoost)

Threshold tuning allowed the model to adapt to clinical priorities (e.g., prioritizing recall over precision).

---

## Model Interpretability

XGBoost feature importance revealed that:
- Admission and discharge details
- Prior utilization history
- Certain diagnosis codes
were among the strongest predictors of readmission.

This supports the clinical validity of the model.

---

## Deployment: Streamlit Application

A **Streamlit web application (`app.py`)** was developed to demonstrate real-world usability.

### Application Features
- Upload a **full CSV file** of patient encounters
- Automatic preprocessing using saved pipeline
- Batch prediction of 30-day readmission risk
- Adjustable classification threshold
- Downloadable prediction results

### Purpose
This application demonstrates how the model could be integrated into:
- Hospital analytics dashboards
- Care management workflows
- Decision support tools

---

## Limitations

- Dataset is dated (1999–2008)
- No direct socioeconomic variables
- No post-discharge intervention data
- Single-encounter modeling (no longitudinal patient history)

---

## Future Work

- Integrate comorbidity indices (e.g., Charlson score)
- Include social determinants of health
- Explore temporal sequence models
- Validate on modern EHR datasets
- Deploy as an API service

---

## Conclusion

This project demonstrates that machine learning models can meaningfully predict 30-day hospital readmissions using encounter-level data. While prediction is imperfect, the results show strong potential for supporting proactive care planning and reducing avoidable readmissions.

By combining rigorous data analysis, multiple modeling strategies, and a deployable application, this project bridges the gap between academic modeling and real-world healthcare impact.

---

## References

- UCI Machine Learning Repository — Diabetes 130-US Hospitals Dataset  
- CMS Hospital Readmissions Reduction Program  
- Scikit-learn, XGBoost, Imbalanced-learn Documentation
