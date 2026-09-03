-- Silver dim_department_hod:
-- Keep as its own lookup (join to dim_department in gold).
-- Trim keys; drop blank rows; rename "Head of Department".
select
    trim(cast(DepartmentID as varchar)) as DepartmentID,
    trim(cast("Head of Department" as varchar)) as HeadOfDepartment
from {{ source('raw', 'dept_hod') }}
where DepartmentID is not null
  and trim(cast(DepartmentID as varchar)) <> ''
  and "Head of Department" is not null
  and trim(cast("Head of Department" as varchar)) <> ''
qualify row_number() over (
    partition by trim(cast(DepartmentID as varchar))
    order by trim(cast("Head of Department" as varchar))
) = 1
order by DepartmentID
