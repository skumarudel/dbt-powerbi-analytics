# Power BI — hospital dashboard

Report file: [`hospital_dashboard.pbix`](hospital_dashboard.pbix)

This report was built entirely in Power BI. The star schema, measures, and pages of **Amrita Research Hospital** all live in the `.pbix`. GitHub does not preview that file, so the screenshots below show the model and the report pages.

The dbt pipeline in this repo (Excel → DuckDB → silver) is a separate check: whether the same cleaning and modeling can be automated, so Power BI can use prepared tables instead of doing that work inside the report.

## Data model

This is the Power BI model. `fact_patientVisits` sits in the center. Department, doctor, patient, payment method, diagnosis, and treatment connect to it, along with a calendar table and a key-measures table. These tables were created in Power BI. They are separate from the dbt silver models.

![Data model](assets/DataTables.png)

## Executive Summary

Hospital-wide snapshot: visit volume, total bill amount, average rating, average wait time, and insurance coverage. Charts break bill amount down by department category, show visits over 2020–2025, split payment methods, compare weekday vs weekend visits, and highlight rush hours by day and hour.

![Executive Summary](assets/Executive_Summary.png)

## Patient Details

Who the patients are: headcount, cities, gender split, and age bands, plus a map of patients by state and city. Buttons switch the bar chart between patients with the most visits and the least.

![Patient Details](assets/Patient_Details.png)

## Doctor Details

One row per doctor: experience, department, patients treated, average wait time, rating, and total bill amount. Filter the table by department category. Conditional icons flag wait time and rating.

![Doctor Details](assets/Dcotor_Details.png)

## Department Details

Department view for the selected category (Internal Medicine in this screenshot): doctor count and average satisfaction, then a table of departments with doctors, experience, bill amount, and bill contribution. Trend charts show bill amount by department over years, and bill amount against visit volume by year.

![Department Details](assets/Department_Details.png)
