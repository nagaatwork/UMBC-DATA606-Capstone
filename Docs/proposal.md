# Project Title: Predicting Hospital Readmissions

### Prepared for  
**UMBC Data Science Master's Capstone**  
Instructor: Dr. Chaojie (Jay) Wang

---

### Author  
**Naga Brahmendra Chowdary Devarapalli**

- GitHub Repository: [https://github.com/nagaatwork/UMBC-DATA606-Capstone](https://github.com/nagaatwork/UMBC-DATA606-Capstone)
- LinkedIn Profile: [https://www.linkedin.com/in/your-linkedin-id](https://www.linkedin.com/in/your-linkedin-id)

---

### Introduction

This project focuses on predicting the probability of hospital readmission within 30 days for diabetic patients using the extensively studied *Diabetes 130-US hospitals (1999–2008)* dataset. Hospital readmissions are an important factor in measuring healthcare quality, and preventing unnecessary readmissions not only improves patient outcomes but also cuts costs. By analysing with demographic details, clinical information, and encounter features, this project opens up a machine learning pipeline to recognize patients at a higher risk of readmission shortly after discharge.

---

### Why Does It Matter?

Readmission rates are not only a clinical concern but also a financial and policy concern. Hospitals face significant penalties from regulatory agencies, such as Medicare and Medicaid, when readmission rates exceed benchmarks. Beyond cost, frequent readmissions often signal gaps in patient care, such as poor discharge planning, inadequate follow-up, or unaddressed comorbidities. Accurately predicting which patients are at risk allows healthcare providers to allocate resources more effectively—such as scheduling follow-up appointments, offering targeted interventions, or providing additional patient education—to reduce avoidable readmissions and improve quality of care.

---

### Research Questions

This project has three main questions it intends to answer:

1. **Do machine learning models have the ability to predict 30-day readmission with reasonable accuracy given encounter-level data?**

2. **Which are the most important factors affecting readmission: demographics, length of stay, lab results, medications, or admission/discharge details?**

3. **How can such a model be incorporated into a useful pipeline that clinicians and hospital administrators can use to assist them with the early identification of high-risk patients?**

---

##  Dataset Overview 

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

### 4. Exploratory Data Analysis (EDA)

---

#### Focus Area
Our target variable is `readmit_30d`, which indicates whether a patient was readmitted within 30 days.

The analysis focuses on:
- Key numeric features: `time_in_hospital`, `num_lab_procedures`, `num_procedures`, `num_medications`, etc.
- Categorical predictors: `age`, `gender`, `race`, `A1Cresult`, `max_glu_serum`, `admission_type_id`, etc.

---

#### Data Quality Checks

- Missing Values:
  - Replaced all "?" values with `NaN`
  - Key columns like `weight`, `payer_code`, and `medical_specialty` had more than 40% missing values and were considered for removal

- Duplicates:
  - No exact duplicate rows were found

---

#### Transformation Requirements

- `age` was converted from range brackets to midpoints
- All numeric columns were converted to appropriate numeric types
- String-type categorical columns will be encoded later

No merging, melting, or pivoting was required at this stage.

---
#### External Data

- No additional data sources like population or Census data were brought in
- However, linking hospital quality ratings or comorbidity scores could enhance the model in future iterations

---
## Target Variable Distribution

- Binary class imbalance:
  - Class 0 (Not readmitted within 30 days): **90.6%**
  - Class 1 (Readmitted within 30 days): **9.4%**

---

## Descriptive Statistics by Readmission

| Variable              | Not Readmitted | Readmitted <30d |
|-----------------------|----------------|-----------------|
| time_in_hospital      | 4.35           | 4.77            |
| num_lab_procedures    | 42.95          | 44.23           |
| num_medications       | 15.91          | 16.90           |
| number_outpatient     | 0.36           | 0.44            |
| number_emergency      | 0.18           | 0.36            |
| number_inpatient      | 0.56           | 1.22            |
| number_diagnoses      | 7.39           | 7.69            |

---

##  Visualizations

### C. Target Variable Visualization — Readmission Status

The bar chart below shows the distribution of the original `readmitted` values:


- **NO** (no readmission): Majority of patients fall into this category.
- **>30** (readmitted after 30 days): Second largest group.
- **<30** (readmitted within 30 days): Smallest group — this is the minority class that we are targeting.

This visualization highlights the **imbalance** in the target variable, which justifies the need for **resampling techniques** like **SMOTE** during model training.

➡️ Based on this, we created a **binary target variable `readmit_30d`**:
- `1` → `<30` days
- `0` → `NO` and `>30`


### B. Categorical Features: Proportions Readmitted

#### A1Cresult
| Category | Proportion Readmitted |
|----------|------------------------|
| >7       | 10.05%                 |
| >8       | 9.87%                  |
| Norm     | 9.65%                  |

#### Max Glucose Serum
| Category | Proportion Readmitted |
|----------|------------------------|
| >200     | 12.46%                 |
| >300     | 14.32%                 |
| Norm     | 11.36%                 |

#### Admission Type ID
| ID | Description        | Readmit % |
|----|--------------------|-----------|
| 1  | Emergency          | 11.5%     |
| 2  | Urgent             | 11.2%     |
| 3  | Elective           | 10.4%     |
| 4  | Newborn            | 10.0%     |
| 5  | Not Available      | 10.3%     |
| 6  | NULL               | 11.1%     |
| 7  | Trauma Center      | 0.0%      |
| 8  | Other              | 8.4%      |

#### Admission Source ID
Top sources with highest readmission:
- ID 22 → 16.7%
- ID 3 → 15.5%
- ID 20 → 13.7%

#### Discharge Disposition ID
Top categories:
- ID 12 (Hospice) → 66.7%
- ID 15 (Short-term hospital) → 44.4%
- ID 9 (Rehab) → 42.9%

---

