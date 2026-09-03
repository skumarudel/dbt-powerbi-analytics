-- Silver fact_patient_visit:
-- 1) union the four year-split raw visit tables
-- 2) trim keys; drop blank VisitID rows
-- 3) VisitDate / DischargeDate as DATE
-- 4) VisitTime as TIME (12-hour AM/PM and 24-hour HH:MM:SS)
-- 5) drop DepartmentCategory (already on dim_department)
with stacked as (
    select * from {{ source('raw', 'patient_visits_2020_2021') }}
    union all
    select * from {{ source('raw', 'patient_visits_2022_2023') }}
    union all
    select * from {{ source('raw', 'patient_visits_2024') }}
    union all
    select * from {{ source('raw', 'patient_visits_2025') }}
),

cleaned as (
    select
        trim(cast(VisitID as varchar)) as VisitID,
        trim(cast(PatientID as varchar)) as PatientID,
        trim(cast(DoctorID as varchar)) as DoctorID,
        trim(cast(DepartmentID as varchar)) as DepartmentID,
        cast(VisitDate as date) as VisitDate,
        case
            when regexp_matches(trim(cast(VisitTime as varchar)), 'AM|PM')
                then cast(
                    strptime(trim(cast(VisitTime as varchar)), '%I:%M %p') as time
                )
            else cast(
                strptime(trim(cast(VisitTime as varchar)), '%H:%M:%S') as time
            )
        end as VisitTime,
        cast(DischargeDate as date) as DischargeDate,
        trim(cast(DiagnosisID as varchar)) as DiagnosisID,
        trim(cast(TreatmentID as varchar)) as TreatmentID,
        BillAmount,
        InsuranceAmount,
        trim(cast(PaymentMethodID as varchar)) as PaymentMethodID,
        SatisfactionScore,
        WaitTimeMinutes
    from stacked
    where VisitID is not null
      and trim(cast(VisitID as varchar)) <> ''
)

select *
from cleaned
order by VisitDate, VisitID
