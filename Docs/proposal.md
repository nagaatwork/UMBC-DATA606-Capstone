

## 3 Dataset Overview – Predicting Hospital Readmissions

### Data Source
- The dataset is sourced from the **UCI Machine Learning Repository**:  
  [Diabetes 130-US hospitals for years 1999–2008 Data Set](https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008)
- It contains de-identified patient records related to diabetes admissions.

### File Information
- **File name:** `diabetic_data.csv`
- **Data size:** ~18 MB
- **Shape:** 101,766 rows × 50 columns
- **Time Period:** 1999–2008
- **Each row represents:** a single hospital encounter for a diabetic patient.

---

### Data Dictionary (Simplified Modeling Subset)

| Column Name               | Data Type | Description                                            | Sample / Categories                     |
|---------------------------|-----------|--------------------------------------------------------|------------------------------------------|
| `admission_id`            | string    | Unique hospital encounter ID                           | e.g., 100006                             |
| `patient_id`              | string    | De-identified patient number                           | e.g., 112186                             |
| `readmit_30d`             | int       | Target: 1 if readmitted within 30 days, else 0         | {0, 1}                                   |
| `age_mid`                 | float     | Midpoint of patient age bracket (from `age`)           | e.g., 65.0 for `[60-70)`                 |
| `gender`                  | category  | Patient gender                                         | `Male`, `Female`, `Unknown`              |
| `race`                    | category  | Patient race                                           | `Caucasian`, `AfricanAmerican`, etc.     |
| `los_days`                | int       | Length of hospital stay (days)                         | e.g., 3, 5                                |
| `num_lab_procedures`      | int       | Number of lab tests during encounter                   | e.g., 40                                 |
| `num_procedures`          | int       | Number of procedures performed                         | e.g., 1, 0                                |
| `num_medications`         | int       | Number of medications prescribed                       | e.g., 13                                 |
| `number_outpatient`       | int       | Outpatient visits in prior year                        | e.g., 0, 2                                |
| `number_emergency`        | int       | Emergency visits in prior year                         | e.g., 0, 1                                |
| `number_inpatient`        | int       | Inpatient visits in prior year                         | e.g., 0, 3                                |
| `number_diagnoses`        | int       | Number of diagnoses recorded                           | e.g., 9                                  |
| `A1Cresult`               | category  | A1C test result for blood sugar control                | `>8`, `Norm`, `None`, `>7`               |
| `max_glu_serum`           | category  | Maximum glucose level measured                         | `>200`, `Norm`, `None`, `>300`           |
| `admission_type_id`       | category  | Type of hospital admission                             | `1`, `2`, ..., `8` (mapped via lookup)   |
| `admission_source_id`     | category  | Source of patient admission                            | `1`, `2`, ..., `25` (mapped via lookup)  |
| `discharge_disposition_id`| category  | Discharge destination or status                        | `1`, `2`, ..., `30` (mapped via lookup)  |

---

### Target Variable
- **`readmit_30d`** — A binary indicator of whether the patient was readmitted within 30 days of discharge.

---

### Feature Variables (Predictors)
The following columns are selected as features for machine learning:
- **Demographics:** `age_mid`, `gender`, `race`
- **Utilization:** `los_days`, `num_lab_procedures`, `num_procedures`, `num_medications`
- **Visit History:** `number_outpatient`, `number_emergency`, `number_inpatient`
- **Clinical Markers:** `number_diagnoses`, `A1Cresult`, `max_glu_serum`
- **Admission Details:** `admission_type_id`, `admission_source_id`, `discharge_disposition_id`

---

### Notes
- Missing values such as `"?"` were replaced with `NaN`.
- Age ranges like `[60-70)` were converted to numeric midpoints.
- Categorical ID columns can be mapped to readable labels using the `IDS_mapping.csv` file.
