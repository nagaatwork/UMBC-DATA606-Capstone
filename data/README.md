# Diabetic Readmission Data

This folder contains the data used for the **UMBC DATA 606** capstone project on 30‑day readmission prediction for patients with diabetes.  
The data are derived from the UCI “Diabetes 130‑US hospitals for years 1999–2008” dataset and include an ID mapping file for categorical codes.[web:100][file:99][file:98]

---

## Files

- `diabetic_data.csv`  
  Main encounter‑level dataset with demographics, utilization, diagnoses, medications, labs, and readmission outcome for diabetic patients.[file:99][web:100]

- `IDS_mapping.csv`  
  Mapping table that translates numeric ID fields (admission type, discharge disposition, admission source) into human‑readable descriptions.[file:98][web:100]

---

## Data Map

### Core columns in `diabetic_data.csv`

Below are some key variables used in the modeling pipeline.[file:99][web:100]

| Column name              | Type        | Description                                                     |
|--------------------------|------------|-----------------------------------------------------------------|
| `encounter_id`           | ID         | Unique hospital encounter identifier                            |
| `patient_nbr`            | ID         | De‑identified patient identifier                                |
| `race`                   | Categorical| Patient race (e.g., Caucasian, AfricanAmerican, Hispanic, ? )   |
| `gender`                 | Categorical| Patient gender                                                  |
| `age`                    | Categorical| 10‑year age band (e.g., 50–60, 70–80)                           |
| `weight`                 | Categorical| Weight in pounds, binned; `?` for missing                       |
| `admission_type_id`      | Integer ID | Type of admission (mapped via `IDS_mapping.csv`)                |
| `discharge_disposition_id` | Integer ID | Discharge destination/status (mapped via `IDS_mapping.csv`)   |
| `admission_source_id`    | Integer ID | Source of admission (mapped via `IDS_mapping.csv`)              |
| `time_in_hospital`       | Numeric    | Length of stay in days                                          |
| `num_lab_procedures`     | Numeric    | Number of lab tests performed during the encounter              |
| `num_procedures`         | Numeric    | Number of procedures performed                                  |
| `num_medications`        | Numeric    | Number of distinct medications administered                     |
| `number_outpatient`      | Numeric    | Outpatient visits in the previous year                          |
| `number_emergency`       | Numeric    | Emergency visits in the previous year                           |
| `number_inpatient`       | Numeric    | Inpatient visits in the previous year                           |
| `diag_1`, `diag_2`, `diag_3` | Categorical | Primary, secondary, tertiary ICD‑9 diagnosis codes       |
| `number_diagnoses`       | Numeric    | Count of distinct diagnoses                                     |
| `max_glu_serum`          | Categorical| Max glucose serum result category (e.g., `None`, `>200`, `>300`)|
| `A1Cresult`              | Categorical| HbA1c result category (`None`, `Norm`, `>7`, `>8`)              |
| Diabetes meds columns    | Categorical| Indicators for specific drugs (e.g., `metformin`, `insulin`, `pioglitazone`, combinations) |
| `change`                 | Categorical| Indicates whether medications were changed during encounter     |
| `diabetesMed`            | Categorical| Indicates if the patient was on any diabetes medication         |
| `readmitted`             | Categorical| Readmission status (`NO`, `>30`, `<30`)                         |

> In the modeling pipeline, `readmitted` is typically converted into a binary label: encounters with `<30` are treated as positive (readmitted within 30 days), while `NO` and `>30` are treated as negative.[web:100][file:99]

---

### ID Mapping (`IDS_mapping.csv`)

`IDS_mapping.csv` provides human‑readable values for the three key ID fields.[file:98][web:100]

**Admission Type (`admission_type_id`) – examples**

- `1` – Emergency  
- `2` – Urgent  
- `3` – Elective  
- `4` – Newborn  
- `5` – Not Available / Unknown  
- `7` – Trauma Center  
- `8` – Not Mapped / Other  

**Discharge Disposition (`discharge_disposition_id`) – examples**

- `1` – Discharged to home  
- `2` – Transferred to another short‑term hospital  
- `3` – Transferred to skilled nursing facility (SNF)  
- `6` – Discharged home with home health service  
- `11` – Expired  
- `13` – Hospice – home  
- `14` – Hospice – medical facility  
- `25` – Not Mapped / Other  

**Admission Source (`admission_source_id`) – examples**

- `1` – Physician referral  
- `2` – Clinic referral  
- `3` – HMO referral  
- `4` – Transfer from another hospital  
- `5` – Transfer from SNF  
- `7` – Emergency room  
- `8` – Court / law enforcement  
- `9` – Not Available / Unknown  

These mappings are used in the notebooks to create grouped features such as `adm_type_grouped` and to make model outputs interpretable.[file:98][file:99]

---

## Usage Notes

- Treat `encounter_id` and `patient_nbr` as identifiers; do not use them directly as numeric features without proper encoding or aggregation.[file:99]  
- The dataset uses placeholders like `?`, `None`, and `NULL` to indicate missing or not mapped values; these should be handled during preprocessing (e.g., imputation, grouping into “Unknown”).[file:99][file:98]  
- When sharing or publishing results, always cite the original UCI Diabetes 130‑US hospitals dataset and associated paper as the primary data source.[web:100]
