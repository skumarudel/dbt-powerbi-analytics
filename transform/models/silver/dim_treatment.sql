-- Light silver pass: treatment is already clean in raw.
-- Keep defensive trim + drop blank keys only.
select
    trim(cast(TreatmentID as varchar)) as TreatmentID,
    trim(cast(TreatmentName as varchar)) as TreatmentName
from {{ source('raw', 'dim_treatment') }}
where TreatmentID is not null and trim(cast(TreatmentID as varchar)) <> ''
  and TreatmentName is not null and trim(cast(TreatmentName as varchar)) <> ''
order by TreatmentID
