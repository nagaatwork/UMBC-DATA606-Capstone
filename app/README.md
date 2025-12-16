# Patient Readmission Predictor

A Streamlit web app that predicts 30‑day readmission risk for diabetic patients using a trained stacking ensemble model.

## App Screenshots

### Single‑Patient Prediction

![Single patient form](images/single_patient.png)

### Batch CSV Prediction

![Batch CSV upload](images/batch_upload.png)


## Features

- **Single Patient tab**
  - Enter age, prior inpatient/emergency/outpatient visits.
  - Specify current hospitalization details: length of stay, number of medications, number of diagnoses, and admission type.
  - Capture diabetes management: HbA1c, glucose, diabetes type, complications, insulin management, medication change, and ICD‑9 diagnoses.
  - App fills in remaining model features with neutral defaults and returns:
    - Readmission probability.
    - High‑risk / low‑risk label based on an optimized F1 threshold.
    - Color‑coded card (red for high risk, green for low risk).

- **Batch Upload (CSV) tab**
  - Upload a CSV file of patient records (up to 200 MB).
  - Missing model columns are added and filled with defaults.
  - Categorical columns (e.g., admission group, diabetes type, insulin status) are cast to fixed category levels.
  - Model outputs:
    - `risk_probability`
    - binary flag `will_readmit`
    - human‑readable `prediction` (`WILL READMIT` vs `Will NOT readmit`)
  - Results are displayed in the app and downloadable as a CSV.

## Model Artifacts

The app uses:

- `stacking_model_pipeline.pkl` – scikit‑learn pipeline with preprocessing and stacking classifier.
- `model_threshold.npy` – stored probability threshold that maximizes F1 score.

Both files must be accessible from the working directory of the Streamlit script.

## Tech Stack

- Python
- Streamlit
- pandas, NumPy
- scikit‑learn
- joblib

## How to Run Locally

