with cleaned as (
    select
        trim(cast(DepartmentID as varchar)) as DepartmentID,
        trim(
            regexp_replace(
                cast(DepartmentName as varchar),
                '(?i)^Dept\s*-\s*',
                ''
            )
        ) as DepartmentName,
        trim(cast(DepartmentCategory as varchar)) as DepartmentCategory
    from {{ source('raw', 'dim_department') }}
),

filtered as (
    select *
    from cleaned
    where DepartmentID is not null and DepartmentID <> ''
      and DepartmentName is not null and DepartmentName <> ''
      and DepartmentCategory is not null and DepartmentCategory <> ''
)

select
    DepartmentID,
    DepartmentName,
    DepartmentCategory
from filtered
qualify row_number() over (
    partition by DepartmentID
    order by DepartmentName, DepartmentCategory
) = 1
order by DepartmentID
