-- Healthcare Readmission & Patient Utilization Analysis: SQL Business Queries

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
