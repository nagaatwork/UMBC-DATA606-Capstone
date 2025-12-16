# Diabetic Patient 30‑Day Readmission Predictor

This project is the **UMBC DATA 606** capstone, focused on predicting whether a hospitalized patient with diabetes will be readmitted within 30 days using electronic health record data.  
It combines a cleaned version of the UCI **“Diabetes 130‑US hospitals for years 1999–2008”** dataset, a stacking‑ensemble machine‑learning model, and a Streamlit web app for interactive risk prediction.[web:100][web:144]

---

## Project Description

Hospital readmissions within 30 days are a major quality and cost concern in diabetes care.  
Patients who are readmitted soon after discharge often have more severe disease, complex medication regimens, and gaps in follow‑up; accurately identifying these high‑risk patients enables earlier intervention and better outcomes.[web:144][web:150][web:102]

Using more than 100,000 inpatient encounters from U.S. hospitals, this project:

- Preprocesses the UCI diabetic readmission dataset, handling missing values and mapping coded fields (e.g., admission type, discharge disposition, admission source) to interpretable categories.[web:100][file:99][file:98]  
- Engineers clinically meaningful features such as prior utilization, length of stay, number of medications, diabetes control markers (A1C, glucose), and insulin/medication change patterns, which prior studies have shown to be important predictors of readmission.[web:144][web:119]  
- Trains and evaluates several machine‑learning models, then deploys a **stacking ensemble** to estimate the probability of 30‑day readmission for each encounter.

The final model and a tuned probability threshold are exposed through a Streamlit app that supports both **single‑patient** and **batch CSV** prediction workflows.

---

## Why This Project Is Useful

### Clinical and operational value

Research has shown that machine‑learning models can meaningfully predict 30‑day readmission risk in patients with diabetes, often highlighting factors such as prior hospitalizations, time in hospital, number of medications, and insulin use as key drivers.[web:144][web:119][web:102]  
When integrated into discharge planning, such models can help:

- **Identify high‑risk patients before they leave the hospital**, so teams can arrange closer outpatient follow‑up, home health visits, telemedicine check‑ins, medication counseling, or social support.[web:144][web:152]  
- **Target limited resources** (e.g., case management, diabetes education, remote monitoring) to those most likely to be readmitted, improving quality of care while reducing preventable readmissions and associated costs.[web:102][web:150]

Although this capstone model is built on de‑identified research data and is **not** a production clinical tool, it demonstrates how a hospital could operationalize readmission risk prediction into a decision‑support workflow.

### Educational and technical value

For data science and ML practitioners, the project provides an end‑to‑end example of:

- Working with a real, messy healthcare dataset that includes missing values, coded categories, and strong class imbalance.[web:100][file:99]  
- Designing a reproducible pipeline: data cleaning, feature engineering, model selection, threshold tuning, and artifact export.  
- Deploying a model as an interactive **Streamlit web application**, including:
  - A user‑friendly single‑patient form with clinically intuitive fields.
  - Batch CSV scoring with downloadable results for population‑level analysis.

---

## Components

- **Data (`data/`)**  
  - `diabetic_data.csv`: main encounter‑level dataset.  
  - `IDS_mapping.csv`: mapping of admission/discharge/source IDs to human‑readable descriptions.[file:99][file:98]

- **Notebook (`notebook/capstonefinal.ipynb`)**  
  - Single, self‑contained notebook that performs EDA, preprocessing, model training, evaluation, threshold selection, and exports the final pipeline and threshold artifacts.

- **Model Artifacts**  
  - `stacking_model_pipeline.pkl`: trained scikit‑learn pipeline (preprocessing + stacking classifier).  
  - `model_threshold.npy`: best F1 decision threshold for converting probabilities to “readmit / not readmit”.

- **Web App (`app.py` or similar)**  
  - Streamlit app providing:
    - Single‑patient prediction with visual risk feedback.  
    - Batch CSV upload, scoring, and result download.

---

## How to Use the Project

1. **Clone and set up**

```
git clone https://github.com/nagaatwork/UMBC-DATA606-Capstone.git
cd UMBC-DATA606-Capstone

python -m venv venv
source venv/bin/activate # on Windows: venv\Scripts\activate

pip install -r requirements.txt
```

2. **Reproduce analysis (optional)**  
- Launch Jupyter and run `notebook/capstonefinal.ipynb` from top to bottom to reproduce EDA, model training, and artifact export using the data in `data/`.[file:99][file:98]

3. **Run the Streamlit app**

```
streamlit run app.py

```

- Use the **Single Patient** tab to experiment with different clinical profiles and see how risk changes.  
- Use the **Batch Upload** tab to score many encounters at once and download predictions for further analysis.

---

## Limitations and Disclaimer

- The model is trained on historical, de‑identified UCI data and has not been externally validated on local hospital EHR data.[web:100][web:144]  
- This project is for **educational and research purposes only** and should not be used for direct clinical decision‑making without rigorous validation, governance, and regulatory review.

Even with these limitations, the project illustrates how modern machine‑learning techniques and simple web tooling can transform raw EHR data into actionable risk scores that support better, more proactive diabetes care.[web:144][web:150][web:102]
