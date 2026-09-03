-- Silver dim_patient:
-- 1) drop NaN / blank key rows
-- 2) FullName from FirstName + LastName (initcap); drop First/Last columns
-- 3) DOB as DATE
-- 4) Gender: M/F -> Male/Female
-- 5) split "City State Country" into City, State, Country (drop original)
with base as (
    select
        trim(cast(PatientID as varchar)) as PatientID,
        {{ initcap('FirstName') }} as FirstName,
        {{ initcap('LastName') }} as LastName,
        cast(DOB as date) as DOB,
        trim(cast(Gender as varchar)) as Gender_raw,
        trim(cast("City State Country" as varchar)) as location_raw
    from {{ source('raw', 'dim_patient') }}
    where PatientID is not null
      and trim(cast(PatientID as varchar)) <> ''
      and FirstName is not null
      and trim(cast(FirstName as varchar)) <> ''
      and LastName is not null
      and trim(cast(LastName as varchar)) <> ''
)

select
    PatientID,
    FirstName || ' ' || LastName as FullName,
    DOB,
    case
        when upper(Gender_raw) = 'M' then 'Male'
        when upper(Gender_raw) = 'F' then 'Female'
        when lower(Gender_raw) = 'male' then 'Male'
        when lower(Gender_raw) = 'female' then 'Female'
        else Gender_raw
    end as Gender,
    trim(split_part(location_raw, ',', 1)) as City,
    trim(split_part(location_raw, ',', 2)) as State,
    trim(split_part(location_raw, ',', 3)) as Country
from base
order by PatientID
