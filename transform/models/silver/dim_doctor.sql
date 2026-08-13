-- Silver dim_doctor:
-- 1) drop fully empty / null-key rows
-- 2) normalize DoctorID: D-17-001 -> D001
-- 3) add FullName = FirstName + LastName
with base as (
    select
        trim(cast(DoctorID as varchar)) as DoctorID_raw,
        trim(cast(FirstName as varchar)) as FirstName,
        trim(cast(LastName as varchar)) as LastName,
        ExperienceYears,
        trim(cast(DepartmentID as varchar)) as DepartmentID,
        trim(cast(Gender as varchar)) as Gender
    from {{ source('raw', 'dim_doctor') }}
    where DoctorID is not null
      and trim(cast(DoctorID as varchar)) <> ''
      and FirstName is not null
      and trim(cast(FirstName as varchar)) <> ''
      and LastName is not null
      and trim(cast(LastName as varchar)) <> ''
)

select
    -- D-17-001 -> D001 (keep D + last segment)
    regexp_replace(DoctorID_raw, '^D-\d+-', 'D') as DoctorID,
    FirstName,
    LastName,
    FirstName || ' ' || LastName as FullName,
    ExperienceYears,
    DepartmentID,
    Gender
from base
order by DoctorID
