import pandas as pd, numpy as np, json, os, textwrap, zipfile
from pathlib import Path
base=Path('/mnt/data/Healthcare_Readmission_Patient_Utilization_Analysis')
raw='/mnt/data/diabetic_data.csv'; mapf='/mnt/data/IDS_mapping.csv'
df=pd.read_csv(raw)
# normalize missing markers
missing_tokens=['?','Unknown/Invalid','Not Available','Not Mapped','None','']
df=df.replace('?', np.nan)
# parse mapping file sections
mp=pd.read_csv(mapf)
sections={}
current='admission_type_id'
rows=[]
for _,r in mp.iterrows():
    key=str(r.iloc[0]) if pd.notna(r.iloc[0]) else None
    desc=r.iloc[1]
    if key in ['admission_type_id','discharge_disposition_id','admission_source_id']:
        if rows: sections[current]=pd.DataFrame(rows, columns=[current,'description'])
        current=key; rows=[]
    elif pd.notna(r.iloc[0]):
        try: rows.append([int(float(r.iloc[0])), desc if pd.notna(desc) else 'Unknown'])
        except: pass
if rows: sections[current]=pd.DataFrame(rows, columns=[current,'description'])
# merge descriptions
for key, m in sections.items():
    m=m.rename(columns={'description': key.replace('_id','_description')})
    df=df.merge(m, on=key, how='left')
# exclude invalid gender and expired/hospice? For operational analysis keep but flag.
df['gender']=df['gender'].replace({'Unknown/Invalid':np.nan})
# readmission flags
df['readmission_status']=df['readmitted'].map({'NO':'Not Readmitted','>30':'Readmitted After 30 Days','<30':'Readmitted Within 30 Days'})
df['readmitted_binary']=df['readmitted'].isin(['<30','>30']).astype(int)
df['readmitted_30_days']=df['readmitted'].eq('<30').astype(int)
# age midpoint/group
age_mid={'[0-10)':5,'[10-20)':15,'[20-30)':25,'[30-40)':35,'[40-50)':45,'[50-60)':55,'[60-70)':65,'[70-80)':75,'[80-90)':85,'[90-100)':95}
df['age_midpoint']=df['age'].map(age_mid)
df['age_group']=pd.cut(df['age_midpoint'], bins=[0,30,50,65,80,120], labels=['Under 30','30-49','50-64','65-79','80+'], right=False)
# LOS category
df['length_of_stay']=df['time_in_hospital']
df['los_category']=pd.cut(df['length_of_stay'], bins=[0,3,7,14,999], labels=['Short Stay (1-3 days)','Medium Stay (4-7 days)','Long Stay (8-14 days)','Very Long Stay (15+ days)'], right=True, include_lowest=True)
# utilization metrics
for c in ['number_outpatient','number_emergency','number_inpatient','num_lab_procedures','num_procedures','num_medications','number_diagnoses']:
    df[c]=pd.to_numeric(df[c], errors='coerce').fillna(0)
df['total_prior_visits']=df['number_outpatient']+df['number_emergency']+df['number_inpatient']
df['total_service_events']=df['num_lab_procedures']+df['num_procedures']+df['num_medications']
# percentile based utilization score 0-100
def pct_rank(s):
    return s.rank(pct=True, method='average')*100
df['utilization_score']=np.round((pct_rank(df['length_of_stay'])*0.25 + pct_rank(df['total_prior_visits'])*0.30 + pct_rank(df['num_lab_procedures'])*0.20 + pct_rank(df['num_medications'])*0.15 + pct_rank(df['num_procedures'])*0.10),2)
df['utilization_segment']=pd.cut(df['utilization_score'], bins=[-1,40,70,85,101], labels=['Low Utilization','Moderate Utilization','High Utilization','Very High Utilization'])
df['high_utilization_flag']=(df['utilization_score']>=85).astype(int)
# complexity score
med_cols=['metformin','repaglinide','nateglinide','chlorpropamide','glimepiride','acetohexamide','glipizide','glyburide','tolbutamide','pioglitazone','rosiglitazone','acarbose','miglitol','troglitazone','tolazamide','examide','citoglipton','insulin','glyburide-metformin','glipizide-metformin','glimepiride-pioglitazone','metformin-rosiglitazone','metformin-pioglitazone']
for c in med_cols:
    if c in df.columns: df[c]=df[c].fillna('No')
df['active_diabetes_med_count']=df[med_cols].apply(lambda r: sum(v!='No' for v in r), axis=1)
df['medication_burden']=pd.cut(df['num_medications'], bins=[-1,10,20,35,999], labels=['Low Medication Burden','Moderate Medication Burden','High Medication Burden','Very High Medication Burden'])
df['patient_complexity_score']=np.round((pct_rank(df['number_diagnoses'])*0.35 + pct_rank(df['active_diabetes_med_count'])*0.20 + pct_rank(df['total_prior_visits'])*0.25 + pct_rank(df['length_of_stay'])*0.20),2)
df['complexity_segment']=pd.cut(df['patient_complexity_score'], bins=[-1,40,70,85,101], labels=['Low Complexity','Moderate Complexity','High Complexity','Very High Complexity'])
# diagnosis grouping from ICD9 diag_1
def diag_group(x):
    if pd.isna(x): return 'Unknown'
    x=str(x).strip()
    if x.startswith('V') or x.startswith('E'): return 'Supplementary/External Cause'
    try: code=float(x)
    except: return 'Unknown'
    if 390 <= code <= 459 or code == 785: return 'Circulatory'
    if 460 <= code <= 519 or code == 786: return 'Respiratory'
    if 520 <= code <= 579 or code == 787: return 'Digestive'
    if 250 <= code < 251: return 'Diabetes'
    if 800 <= code <= 999: return 'Injury/Poisoning'
    if 710 <= code <= 739: return 'Musculoskeletal'
    if 580 <= code <= 629 or code == 788: return 'Genitourinary'
    if 140 <= code <= 239: return 'Neoplasms'
    return 'Other'
df['primary_diagnosis_group']=df['diag_1'].apply(diag_group)
# admission/discharge categories
expired_ids={11,19,20,21}
hospice_ids={13,14}
df['expired_flag']=df['discharge_disposition_id'].isin(expired_ids).astype(int)
df['hospice_flag']=df['discharge_disposition_id'].isin(hospice_ids).astype(int)
df['admission_category']=df['admission_type_description'].fillna('Unknown')
df['admission_source_category']=df['admission_source_description'].fillna('Unknown')
df['discharge_category']=df['discharge_disposition_description'].fillna('Unknown')
# financial simulation
AVG_BED_DAY_COST=2500; AVG_READMISSION_COST=15000
df['estimated_encounter_cost']=df['length_of_stay']*AVG_BED_DAY_COST + df['num_procedures']*1200 + df['num_lab_procedures']*75 + df['num_medications']*35
df['estimated_readmission_cost_exposure']=df['readmitted_30_days']*AVG_READMISSION_COST
# drop duplicates encounter, keep first
df=df.drop_duplicates(subset=['encounter_id'])
# save raw copies
pd.read_csv(raw).to_csv(base/'data'/'diabetic_data_raw.csv', index=False)
pd.read_csv(mapf).to_csv(base/'data'/'IDS_mapping.csv', index=False)
# select columns for cleaned
cols=['encounter_id','patient_nbr','race','gender','age','age_midpoint','age_group','admission_type_id','admission_category','admission_source_id','admission_source_category','discharge_disposition_id','discharge_category','medical_specialty','primary_diagnosis_group','diag_1','diag_2','diag_3','length_of_stay','los_category','num_lab_procedures','num_procedures','num_medications','number_diagnoses','number_outpatient','number_emergency','number_inpatient','total_prior_visits','total_service_events','utilization_score','utilization_segment','high_utilization_flag','active_diabetes_med_count','medication_burden','patient_complexity_score','complexity_segment','diabetesMed','change','readmitted','readmission_status','readmitted_binary','readmitted_30_days','expired_flag','hospice_flag','estimated_encounter_cost','estimated_readmission_cost_exposure']
clean=df[cols].copy()
clean.to_csv(base/'data'/'healthcare_readmission_utilization_cleaned.csv', index=False)
# summary metrics
summary={
 'total_encounters': int(len(clean)),
 'unique_patients': int(clean['patient_nbr'].nunique()),
 'readmitted_any': int(clean['readmitted_binary'].sum()),
 'readmission_rate_any': float(round(clean['readmitted_binary'].mean()*100,2)),
 'readmitted_30_days': int(clean['readmitted_30_days'].sum()),
 'readmission_rate_30_days': float(round(clean['readmitted_30_days'].mean()*100,2)),
 'avg_length_of_stay': float(round(clean['length_of_stay'].mean(),2)),
 'high_utilization_patients': int(clean['high_utilization_flag'].sum()),
 'high_utilization_rate': float(round(clean['high_utilization_flag'].mean()*100,2)),
 'estimated_total_encounter_cost': float(round(clean['estimated_encounter_cost'].sum(),2)),
 'estimated_30_day_readmission_cost_exposure': float(round(clean['estimated_readmission_cost_exposure'].sum(),2)),
}
(base/'reports'/'summary_metrics.json').write_text(json.dumps(summary, indent=2))
# aggregate insights
read_by_age=clean.groupby('age_group', observed=True)['readmitted_30_days'].mean().mul(100).round(2).sort_values(ascending=False)
read_by_diag=clean.groupby('primary_diagnosis_group')['readmitted_30_days'].agg(['count','mean']).assign(rate=lambda x:(x['mean']*100).round(2)).sort_values('rate',ascending=False)
read_by_adm=clean.groupby('admission_category')['readmitted_30_days'].agg(['count','mean']).assign(rate=lambda x:(x['mean']*100).round(2)).sort_values('rate',ascending=False)
util=clean.groupby('utilization_segment', observed=True).agg(encounters=('encounter_id','count'), readmission_rate_30=('readmitted_30_days','mean'), avg_los=('length_of_stay','mean'), avg_cost=('estimated_encounter_cost','mean')).round(2)
# files text
insights=f'''# Insights — Healthcare Readmission & Patient Utilization Analysis

## Executive Summary
- Total hospital encounters analyzed: **{summary['total_encounters']:,}**
- Unique patients: **{summary['unique_patients']:,}**
- Any readmission rate: **{summary['readmission_rate_any']}%**
- 30-day readmission rate: **{summary['readmission_rate_30_days']}%**
- Average length of stay: **{summary['avg_length_of_stay']} days**
- High-utilization encounters: **{summary['high_utilization_patients']:,}** (**{summary['high_utilization_rate']}%**)
- Estimated 30-day readmission cost exposure: **${summary['estimated_30_day_readmission_cost_exposure']:,.0f}**

## Key Findings
1. **Readmission is not evenly distributed across patients.** High-utilization and high-complexity patients show higher operational burden through longer stays, more procedures, and more prior visits.
2. **30-day readmissions are a stronger operational KPI than any readmission.** The project separates `<30`, `>30`, and `NO` readmissions to support hospital quality analysis.
3. **Length of stay and prior utilization are important operational indicators.** The engineered utilization score combines hospital stay, outpatient visits, emergency visits, inpatient visits, labs, procedures, and medications.
4. **Patient complexity can be analyzed without building a duplicate churn-style model.** Complexity is measured using diagnosis count, medication activity, prior visits, and hospital stay.
5. **Cost exposure can be simulated.** This project estimates encounter cost and 30-day readmission cost exposure using transparent assumptions.

## Readmission by Age Group
{read_by_age.to_string()}

## Readmission by Primary Diagnosis Group
{read_by_diag[['count','rate']].head(10).to_string()}

## Readmission by Admission Type
{read_by_adm[['count','rate']].head(10).to_string()}

## Utilization Segment Summary
{util.to_string()}

## Recommended Actions
- Prioritize follow-up programs for patients with high utilization scores and multiple prior inpatient/emergency visits.
- Monitor 30-day readmission rates by age group, diagnosis group, admission type, and discharge destination.
- Use complexity and utilization segmentation to support care coordination and resource planning.
- Track length-of-stay categories to identify operational bottlenecks and high-cost patient cohorts.
'''
(base/'reports'/'insights.md').write_text(insights)
readme=f'''# Healthcare Readmission & Patient Utilization Analysis

## Project Overview
This project analyzes hospital encounter data to understand patient readmissions, healthcare utilization, patient complexity, and operational resource consumption. It uses the UCI Diabetes 130-US hospitals dataset and transforms raw coded healthcare fields into business-ready metrics for SQL analysis and BI dashboarding.

## Business Objective
Hospitals need to understand which patient groups drive readmissions and resource utilization. This project identifies patterns in 30-day readmissions, length of stay, prior visits, medication burden, diagnosis groups, and patient complexity to support operational and clinical decision-making.

## Tools Used
- Python: data cleaning, feature engineering, exploratory analysis
- SQL: healthcare business queries and KPI validation
- Tableau / Power BI: executive dashboard design
- GitHub: portfolio documentation and project versioning

## Dataset
Main dataset: `diabetic_data.csv`  
Mapping file: `IDS_mapping.csv`

The raw dataset contains **{summary['total_encounters']:,} hospital encounters** and **{summary['unique_patients']:,} unique patients**.

## Engineered Features
- `readmitted_binary`
- `readmitted_30_days`
- `length_of_stay`
- `los_category`
- `total_prior_visits`
- `total_service_events`
- `utilization_score`
- `utilization_segment`
- `high_utilization_flag`
- `active_diabetes_med_count`
- `medication_burden`
- `patient_complexity_score`
- `complexity_segment`
- `primary_diagnosis_group`
- `estimated_encounter_cost`
- `estimated_readmission_cost_exposure`

## Key KPIs
- Total encounters: **{summary['total_encounters']:,}**
- Unique patients: **{summary['unique_patients']:,}**
- Any readmission rate: **{summary['readmission_rate_any']}%**
- 30-day readmission rate: **{summary['readmission_rate_30_days']}%**
- Average length of stay: **{summary['avg_length_of_stay']} days**
- High-utilization rate: **{summary['high_utilization_rate']}%**
- Estimated 30-day readmission cost exposure: **${summary['estimated_30_day_readmission_cost_exposure']:,.0f}**

## Repository Structure
```text
Healthcare_Readmission_Patient_Utilization_Analysis/
├── data/
│   ├── diabetic_data_raw.csv
│   ├── IDS_mapping.csv
│   └── healthcare_readmission_utilization_cleaned.csv
├── notebooks/
│   └── healthcare_readmission_utilization_analysis.ipynb
├── sql/
│   ├── create_tables.sql
│   └── healthcare_business_queries.sql
├── dashboard/
│   └── dashboard_requirements.md
├── reports/
│   ├── insights.md
│   ├── data_dictionary.md
│   └── summary_metrics.json
└── README.md
```

## Dashboard Pages
1. Executive Overview
2. Readmission Analysis
3. Patient Utilization Analysis
4. Patient Complexity & Cohorts
5. Financial Impact Simulation

## Portfolio Summary
Built an end-to-end healthcare analytics project analyzing hospital readmissions, patient utilization, and operational resource consumption. Engineered utilization and complexity scores, created SQL business queries, and designed dashboard requirements to support healthcare decision-making.
'''
(base/'README.md').write_text(readme)
# data dictionary
entries={c:'' for c in clean.columns}
custom={
'encounter_id':'Unique hospital encounter identifier.','patient_nbr':'Unique patient identifier.','admission_category':'Readable admission type joined from IDS mapping.','admission_source_category':'Readable admission source joined from IDS mapping.','discharge_category':'Readable discharge disposition joined from IDS mapping.','length_of_stay':'Hospital stay duration in days, sourced from time_in_hospital.','readmitted_30_days':'1 if patient was readmitted within 30 days, else 0.','readmitted_binary':'1 if patient was readmitted either within or after 30 days, else 0.','total_prior_visits':'Sum of prior outpatient, emergency, and inpatient visits.','total_service_events':'Sum of lab procedures, procedures, and medications.','utilization_score':'Percentile-based operational utilization score from LOS, visits, labs, medications, and procedures.','utilization_segment':'Low, moderate, high, or very high utilization segment.','high_utilization_flag':'1 if utilization score is 85 or higher.','patient_complexity_score':'Percentile-based score combining diagnoses, active diabetes medications, prior visits, and LOS.','complexity_segment':'Low, moderate, high, or very high patient complexity segment.','estimated_encounter_cost':'Simulated cost using bed-day, procedure, lab, and medication assumptions.','estimated_readmission_cost_exposure':'Simulated cost exposure for 30-day readmissions.'}
entries.update(custom)
dd='# Data Dictionary\n\n| Column | Description |\n|---|---|\n'+'\n'.join([f'| `{c}` | {entries[c]} |' for c in clean.columns])
(base/'reports'/'data_dictionary.md').write_text(dd)
# SQL create + queries
create='''CREATE TABLE healthcare_readmission_utilization (
    encounter_id BIGINT,
    patient_nbr BIGINT,
    race VARCHAR(50),
    gender VARCHAR(30),
    age VARCHAR(20),
    age_midpoint INT,
    age_group VARCHAR(30),
    admission_type_id INT,
    admission_category VARCHAR(100),
    admission_source_id INT,
    admission_source_category VARCHAR(150),
    discharge_disposition_id INT,
    discharge_category VARCHAR(200),
    medical_specialty VARCHAR(150),
    primary_diagnosis_group VARCHAR(100),
    diag_1 VARCHAR(20),
    diag_2 VARCHAR(20),
    diag_3 VARCHAR(20),
    length_of_stay INT,
    los_category VARCHAR(50),
    num_lab_procedures INT,
    num_procedures INT,
    num_medications INT,
    number_diagnoses INT,
    number_outpatient INT,
    number_emergency INT,
    number_inpatient INT,
    total_prior_visits INT,
    total_service_events INT,
    utilization_score DECIMAL(6,2),
    utilization_segment VARCHAR(50),
    high_utilization_flag INT,
    active_diabetes_med_count INT,
    medication_burden VARCHAR(50),
    patient_complexity_score DECIMAL(6,2),
    complexity_segment VARCHAR(50),
    diabetesMed VARCHAR(10),
    change VARCHAR(10),
    readmitted VARCHAR(10),
    readmission_status VARCHAR(50),
    readmitted_binary INT,
    readmitted_30_days INT,
    expired_flag INT,
    hospice_flag INT,
    estimated_encounter_cost DECIMAL(12,2),
    estimated_readmission_cost_exposure DECIMAL(12,2)
);
'''
(base/'sql'/'create_tables.sql').write_text(create)
queries='''-- Healthcare Readmission & Patient Utilization Analysis: SQL Business Queries

-- 1. Executive KPI Summary
SELECT
    COUNT(*) AS total_encounters,
    COUNT(DISTINCT patient_nbr) AS unique_patients,
    ROUND(AVG(readmitted_binary) * 100, 2) AS any_readmission_rate,
    ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate,
    ROUND(AVG(length_of_stay), 2) AS avg_length_of_stay,
    ROUND(AVG(high_utilization_flag) * 100, 2) AS high_utilization_rate,
    ROUND(SUM(estimated_readmission_cost_exposure), 2) AS readmission_cost_exposure
FROM healthcare_readmission_utilization;

-- 2. Readmission rate by age group
SELECT age_group, COUNT(*) AS encounters,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate
FROM healthcare_readmission_utilization
GROUP BY age_group
ORDER BY readmission_30_day_rate DESC;

-- 3. Readmission rate by primary diagnosis group
SELECT primary_diagnosis_group, COUNT(*) AS encounters,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate
FROM healthcare_readmission_utilization
GROUP BY primary_diagnosis_group
ORDER BY readmission_30_day_rate DESC;

-- 4. Utilization segment performance
SELECT utilization_segment, COUNT(*) AS encounters,
       ROUND(AVG(length_of_stay), 2) AS avg_los,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate,
       ROUND(AVG(estimated_encounter_cost), 2) AS avg_estimated_cost
FROM healthcare_readmission_utilization
GROUP BY utilization_segment
ORDER BY avg_estimated_cost DESC;

-- 5. Complexity segment performance
SELECT complexity_segment, COUNT(*) AS encounters,
       ROUND(AVG(total_prior_visits), 2) AS avg_prior_visits,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate,
       ROUND(SUM(estimated_encounter_cost), 2) AS total_estimated_cost
FROM healthcare_readmission_utilization
GROUP BY complexity_segment
ORDER BY total_estimated_cost DESC;

-- 6. Length of stay category and readmissions
SELECT los_category, COUNT(*) AS encounters,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate,
       ROUND(SUM(estimated_encounter_cost), 2) AS total_estimated_cost
FROM healthcare_readmission_utilization
GROUP BY los_category;

-- 7. Admission type analysis
SELECT admission_category, COUNT(*) AS encounters,
       ROUND(AVG(length_of_stay), 2) AS avg_los,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate
FROM healthcare_readmission_utilization
GROUP BY admission_category
ORDER BY encounters DESC;

-- 8. Emergency utilization and readmission
SELECT number_emergency, COUNT(*) AS encounters,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate
FROM healthcare_readmission_utilization
GROUP BY number_emergency
ORDER BY number_emergency;

-- 9. Medication burden analysis
SELECT medication_burden, COUNT(*) AS encounters,
       ROUND(AVG(num_medications), 2) AS avg_medications,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate
FROM healthcare_readmission_utilization
GROUP BY medication_burden
ORDER BY avg_medications DESC;

-- 10. Top medical specialties by encounter count
SELECT medical_specialty, COUNT(*) AS encounters,
       ROUND(AVG(length_of_stay), 2) AS avg_los,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate
FROM healthcare_readmission_utilization
WHERE medical_specialty IS NOT NULL
GROUP BY medical_specialty
ORDER BY encounters DESC
LIMIT 15;

-- 11. Cost exposure by diagnosis group
SELECT primary_diagnosis_group,
       COUNT(*) AS encounters,
       ROUND(SUM(estimated_encounter_cost), 2) AS total_estimated_cost,
       ROUND(SUM(estimated_readmission_cost_exposure), 2) AS readmission_cost_exposure
FROM healthcare_readmission_utilization
GROUP BY primary_diagnosis_group
ORDER BY readmission_cost_exposure DESC;

-- 12. High-utilization patients by age group
SELECT age_group, COUNT(*) AS encounters,
       SUM(high_utilization_flag) AS high_utilization_encounters,
       ROUND(AVG(high_utilization_flag) * 100, 2) AS high_utilization_rate
FROM healthcare_readmission_utilization
GROUP BY age_group
ORDER BY high_utilization_rate DESC;

-- 13. Diabetes medication status and readmission
SELECT diabetesMed, COUNT(*) AS encounters,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate,
       ROUND(AVG(active_diabetes_med_count), 2) AS avg_active_diabetes_med_count
FROM healthcare_readmission_utilization
GROUP BY diabetesMed;

-- 14. Prior inpatient visits and readmission
SELECT number_inpatient, COUNT(*) AS encounters,
       ROUND(AVG(readmitted_30_days) * 100, 2) AS readmission_30_day_rate
FROM healthcare_readmission_utilization
GROUP BY number_inpatient
ORDER BY number_inpatient;

-- 15. Patient-level repeat encounter summary
SELECT patient_nbr,
       COUNT(*) AS total_encounters,
       SUM(readmitted_30_days) AS thirty_day_readmissions,
       ROUND(AVG(utilization_score), 2) AS avg_utilization_score,
       ROUND(AVG(patient_complexity_score), 2) AS avg_complexity_score
FROM healthcare_readmission_utilization
GROUP BY patient_nbr
HAVING COUNT(*) > 1
ORDER BY total_encounters DESC, thirty_day_readmissions DESC;
'''
(base/'sql'/'healthcare_business_queries.sql').write_text(queries)
# dashboard requirements
(base/'dashboard'/'dashboard_requirements.md').write_text(f'''# Dashboard Requirements

## Dashboard Title
Healthcare Readmission & Patient Utilization Analysis

## Data Source
`data/healthcare_readmission_utilization_cleaned.csv`

## Page 1 — Executive Overview
KPI Cards:
- Total Encounters
- Unique Patients
- 30-Day Readmission Rate
- Any Readmission Rate
- Average Length of Stay
- High Utilization Rate
- Estimated 30-Day Readmission Cost Exposure

Recommended visuals:
- Readmission status distribution
- Encounters by age group
- Average length of stay by age group
- Cost exposure by primary diagnosis group

## Page 2 — Readmission Analysis
Visuals:
- 30-day readmission rate by age group
- 30-day readmission rate by diagnosis group
- Readmission rate by admission category
- Readmission rate by discharge category

## Page 3 — Patient Utilization
Visuals:
- Utilization segment distribution
- Average LOS by utilization segment
- Prior visits vs readmission rate
- Emergency visits vs readmission rate

## Page 4 — Patient Complexity
Visuals:
- Complexity segment distribution
- Readmission rate by complexity segment
- Medication burden by age group
- Number of diagnoses by diagnosis group

## Page 5 — Financial Impact
Visuals:
- Estimated encounter cost by diagnosis group
- Readmission cost exposure by age group
- Cost by utilization segment
- Savings scenario: reduce 30-day readmissions by 10%, 15%, and 20%

## Calculated Fields for Tableau
- 30-Day Readmission Rate = AVG([readmitted_30_days])
- Any Readmission Rate = AVG([readmitted_binary])
- High Utilization Rate = AVG([high_utilization_flag])
- Total Estimated Cost = SUM([estimated_encounter_cost])
- Readmission Cost Exposure = SUM([estimated_readmission_cost_exposure])
- Average LOS = AVG([length_of_stay])

## Suggested Filters
- Age Group
- Gender
- Race
- Admission Category
- Diagnosis Group
- Utilization Segment
- Complexity Segment
''')
# python script
script = Path('/mnt/data/build_healthcare_project.py').read_text()
(base/'notebooks'/'healthcare_readmission_utilization_analysis.py').write_text(script)
# Create ipynb with same script as chunks
import nbformat as nbf
nb=nbf.v4.new_notebook()
nb['cells']=[nbf.v4.new_markdown_cell('# Healthcare Readmission & Patient Utilization Analysis\n\nThis notebook cleans the raw UCI Diabetes hospital encounter dataset and creates utilization/readmission analytics features.'), nbf.v4.new_code_cell(script)]
nbf.write(nb, base/'notebooks'/'healthcare_readmission_utilization_analysis.ipynb')
# zip
zip_path=Path('/mnt/data/Healthcare_Readmission_Patient_Utilization_Analysis.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for file in base.rglob('*'):
        z.write(file, file.relative_to(base.parent))
print(json.dumps(summary, indent=2))
print('Created', zip_path)
