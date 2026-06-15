# Dashboard Requirements

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
