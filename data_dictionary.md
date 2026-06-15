# Data Dictionary

| Column | Description |
|---|---|
| `encounter_id` | Unique hospital encounter identifier. |
| `patient_nbr` | Unique patient identifier. |
| `race` |  |
| `gender` |  |
| `age` |  |
| `age_midpoint` |  |
| `age_group` |  |
| `admission_type_id` |  |
| `admission_category` | Readable admission type joined from IDS mapping. |
| `admission_source_id` |  |
| `admission_source_category` | Readable admission source joined from IDS mapping. |
| `discharge_disposition_id` |  |
| `discharge_category` | Readable discharge disposition joined from IDS mapping. |
| `medical_specialty` |  |
| `primary_diagnosis_group` |  |
| `diag_1` |  |
| `diag_2` |  |
| `diag_3` |  |
| `length_of_stay` | Hospital stay duration in days, sourced from time_in_hospital. |
| `los_category` |  |
| `num_lab_procedures` |  |
| `num_procedures` |  |
| `num_medications` |  |
| `number_diagnoses` |  |
| `number_outpatient` |  |
| `number_emergency` |  |
| `number_inpatient` |  |
| `total_prior_visits` | Sum of prior outpatient, emergency, and inpatient visits. |
| `total_service_events` | Sum of lab procedures, procedures, and medications. |
| `utilization_score` | Percentile-based operational utilization score from LOS, visits, labs, medications, and procedures. |
| `utilization_segment` | Low, moderate, high, or very high utilization segment. |
| `high_utilization_flag` | 1 if utilization score is 85 or higher. |
| `active_diabetes_med_count` |  |
| `medication_burden` |  |
| `patient_complexity_score` | Percentile-based score combining diagnoses, active diabetes medications, prior visits, and LOS. |
| `complexity_segment` | Low, moderate, high, or very high patient complexity segment. |
| `diabetesMed` |  |
| `change` |  |
| `readmitted` |  |
| `readmission_status` |  |
| `readmitted_binary` | 1 if patient was readmitted either within or after 30 days, else 0. |
| `readmitted_30_days` | 1 if patient was readmitted within 30 days, else 0. |
| `expired_flag` |  |
| `hospice_flag` |  |
| `estimated_encounter_cost` | Simulated cost using bed-day, procedure, lab, and medication assumptions. |
| `estimated_readmission_cost_exposure` | Simulated cost exposure for 30-day readmissions. |