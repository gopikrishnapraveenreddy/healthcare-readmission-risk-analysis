# Healthcare Readmission Risk Analysis

## Healthcare Readmission & Patient Utilization Analytics Platform

### Identifying High-Risk Patient Segments, Healthcare Resource Utilization, and Financial Exposure

This project presents an end-to-end healthcare analytics solution built using Python, SQL, and Tableau to analyze hospital readmission patterns, evaluate healthcare resource utilization, and quantify the financial impact of patient readmissions.

The analysis leverages over 100,000 healthcare encounters to uncover high-risk patient populations, operational utilization trends, patient complexity patterns, and readmission cost exposure. The resulting insights support healthcare administrators in improving patient outcomes, optimizing resource allocation, and reducing avoidable healthcare costs.

---

## Business Problem

Hospital readmissions represent a significant challenge for healthcare providers due to their impact on:

* Patient outcomes and quality of care
* Hospital resource utilization
* Operational efficiency
* Healthcare expenditures
* Regulatory and performance metrics

The objective of this project is to:

* Analyze 30-day hospital readmissions
* Identify high-risk patient segments
* Understand key drivers of readmission risk
* Evaluate healthcare utilization patterns
* Measure patient complexity and resource consumption
* Quantify financial exposure associated with readmissions
* Support data-driven healthcare decision-making

---

## Project Highlights

* Analyzed **101,766 healthcare encounters** across **71,518 unique patients**
* Evaluated readmission patterns across demographic, clinical, admission, and discharge categories
* Identified patient populations associated with elevated readmission risk
* Developed healthcare utilization segmentation framework
* Quantified **$170.36M** in estimated readmission cost exposure
* Measured patient complexity and healthcare resource consumption patterns
* Built **three executive Tableau dashboards** for operational and strategic healthcare reporting
* Performed SQL-based healthcare reporting and KPI analysis

---

## Tools & Technologies

| Category                | Technologies            |
| ----------------------- | ----------------------- |
| Programming             | Python                  |
| Data Processing         | Pandas, NumPy           |
| Database                | SQL                     |
| Visualization           | Tableau                 |
| Analytics               | Healthcare KPI Analysis |
| Development Environment | Jupyter Notebook        |
| Version Control         | GitHub                  |

---

## Key Performance Indicators

| KPI                                 | Value    |
| ----------------------------------- | -------- |
| Total Encounters                    | 101,766  |
| Unique Patients                     | 71,518   |
| Readmitted Within 30 Days           | 11,357   |
| 30-Day Readmission Rate             | 11.16%   |
| Average Patient Complexity Score    | 50.0     |
| High Utilization Rate               | 1.61%    |
| Estimated Readmission Cost Exposure | $170.36M |

---

## Dashboard 1: Healthcare Readmission & Patient Utilization Analysis

### Objective

Provide an executive-level overview of healthcare operations, patient utilization, and readmission performance.

### Key Insights

* Overall 30-day readmission rate reached 11.16%
* More than 11,000 encounters resulted in readmission within 30 days
* Older patient populations represented a substantial portion of healthcare utilization
* Readmissions contributed significantly to overall healthcare cost exposure
* High-utilization patients required disproportionate healthcare resources

![Dashboard 1](Healthcare%20Readmission%20%26%20Patient%20Utilization%20Analysis.png)

---

## Dashboard 2: Healthcare Readmission Analysis

### Objective

Identify patient segments and healthcare factors associated with elevated readmission rates.

### Key Insights

* Patients aged 80+ demonstrated the highest readmission risk
* Emergency admissions generated the highest readmission rates
* Diabetes and chronic disease-related diagnosis groups exhibited increased readmission levels
* Diagnosis category significantly influenced readmission outcomes
* Discharge disposition was strongly associated with future readmission likelihood

![Dashboard 2](Healthcare%20Readmission%20Analysis.png)

---

## Dashboard 3: Healthcare Resource Utilization & Cost Exposure Analysis

### Objective

Analyze healthcare resource consumption, patient complexity, and financial impact across patient populations.

### Key Insights

* Healthcare cost exposure increased significantly among older age groups
* Patient complexity scores consistently rose with age
* Moderate-utilization patients represented the largest utilization segment
* Certain diagnosis groups required substantially longer hospital stays
* Readmissions generated considerable financial burden across the healthcare system

![Dashboard 3](Healthcare%20Resource%20Utilization%20%26%20Cost%20Exposure%20Analysis.png)

---

## Analytical Workflow

### Data Preparation

* Data cleaning and preprocessing
* Missing value treatment
* Feature engineering
* Healthcare category mapping
* Data validation and quality checks

### SQL Analytics

* Readmission KPI reporting
* Patient utilization analysis
* Cost exposure calculations
* Operational healthcare reporting

### Tableau Dashboard Development

* Executive KPI dashboards
* Readmission risk analysis
* Utilization monitoring
* Financial impact reporting

---

## Repository Structure

```text
healthcare-readmission-risk-analysis
│
├── Healthcare_Readmission_And_Utilization_Analysis.twb
├── healthcare_readmission_utilization_analysis.ipynb
├── healthcare_readmission_utilization_analysis.py
│
├── create_tables.sql
├── healthcare_business_queries.sql
│
├── diabetic_data_raw.csv
├── IDS_mapping.csv
│
├── data_dictionary.md
├── insights.md
├── summary_metrics.json
│
├── Healthcare Readmission & Patient Utilization Analysis.png
├── Healthcare Readmission Analysis.png
├── Healthcare Resource Utilization & Cost Exposure Analysis.png
│
└── dashboard_requirements.md
```

---

## Business Value

This solution enables healthcare organizations to:

* Monitor and reduce avoidable readmissions
* Identify high-risk patient populations
* Improve patient outcome management
* Optimize healthcare resource allocation
* Monitor utilization trends across patient segments
* Understand the financial impact of readmissions
* Support strategic healthcare planning and operational decision-making

---

## Author

**Gopi Krishna Praveen Reddy Doranala**

Master of Science in Business Analytics
University of North Texas

### Skills Demonstrated

Healthcare Analytics • Tableau • SQL • Python • Data Visualization • Business Intelligence • KPI Reporting • Healthcare Operations Analytics • Data Analysis • Dashboard Development
