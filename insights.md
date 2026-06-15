# Insights — Healthcare Readmission & Patient Utilization Analysis

## Executive Summary
- Total hospital encounters analyzed: **101,766**
- Unique patients: **71,518**
- Any readmission rate: **46.09%**
- 30-day readmission rate: **11.16%**
- Average length of stay: **4.4 days**
- High-utilization encounters: **1,634** (**1.61%**)
- Estimated 30-day readmission cost exposure: **$170,355,000**

## Key Findings
1. **Readmission is not evenly distributed across patients.** High-utilization and high-complexity patients show higher operational burden through longer stays, more procedures, and more prior visits.
2. **30-day readmissions are a stronger operational KPI than any readmission.** The project separates `<30`, `>30`, and `NO` readmissions to support hospital quality analysis.
3. **Length of stay and prior utilization are important operational indicators.** The engineered utilization score combines hospital stay, outpatient visits, emergency visits, inpatient visits, labs, procedures, and medications.
4. **Patient complexity can be analyzed without building a duplicate churn-style model.** Complexity is measured using diagnosis count, medication activity, prior visits, and hospital stay.
5. **Cost exposure can be simulated.** This project estimates encounter cost and 30-day readmission cost exposure using transparent assumptions.

## Readmission by Age Group
age_group
80+         11.95
65-79       11.47
Under 30    11.12
30-49       10.78
50-64        9.67

## Readmission by Primary Diagnosis Group
                              count   rate
primary_diagnosis_group                   
Unknown                          21  23.81
Supplementary/External Cause   1645  16.17
Diabetes                       8757  12.98
Injury/Poisoning               6974  12.25
Circulatory                   30437  11.45
Other                         16527  11.01
Genitourinary                  5117  10.85
Digestive                      9475  10.71
Neoplasms                      3433  10.08
Respiratory                   14423   9.73

## Readmission by Admission Type
                    count   rate
admission_category              
Emergency           53990  11.52
Urgent              18480  11.18
Unknown              5291  11.08
Elective            18869  10.39
Not Available        4785  10.34
Newborn                10  10.00
Not Mapped            320   8.44
Trauma Center          21   0.00

## Utilization Segment Summary
                       encounters  readmission_rate_30  avg_los  avg_cost
utilization_segment                                                      
Low Utilization             30285                 0.08     2.13   9029.39
Moderate Utilization        58625                 0.12     4.73  17447.09
High Utilization            11227                 0.16     7.93  27942.02
Very High Utilization        1629                 0.19    10.12  35609.57

## Recommended Actions
- Prioritize follow-up programs for patients with high utilization scores and multiple prior inpatient/emergency visits.
- Monitor 30-day readmission rates by age group, diagnosis group, admission type, and discharge destination.
- Use complexity and utilization segmentation to support care coordination and resource planning.
- Track length-of-stay categories to identify operational bottlenecks and high-cost patient cohorts.
