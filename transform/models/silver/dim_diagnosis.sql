-- Light silver pass: diagnosis is already clean in raw.
-- Keep defensive trim + drop blank keys only.
select
    trim(cast(DiagnosisID as varchar)) as DiagnosisID,
    trim(cast(DiagnosisName as varchar)) as DiagnosisName
from {{ source('raw', 'dim_diagnosis') }}
where DiagnosisID is not null and trim(cast(DiagnosisID as varchar)) <> ''
  and DiagnosisName is not null and trim(cast(DiagnosisName as varchar)) <> ''
order by DiagnosisID
