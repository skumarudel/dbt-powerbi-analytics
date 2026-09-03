-- Silver dim_payment_method:
-- Raw sheet is transactions (72 rows). Collapse to one row per method.
select
    trim(cast(PaymentMethodID as varchar)) as PaymentMethodID,
    trim(cast(PaymentMethod as varchar)) as PaymentMethod
from {{ source('raw', 'dim_payment_method') }}
where PaymentMethodID is not null
  and trim(cast(PaymentMethodID as varchar)) <> ''
  and PaymentMethod is not null
  and trim(cast(PaymentMethod as varchar)) <> ''
group by
    trim(cast(PaymentMethodID as varchar)),
    trim(cast(PaymentMethod as varchar))
order by PaymentMethodID
