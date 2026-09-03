{% macro initcap(expr) %}
{# DuckDB has no initcap(); title-case each space-separated word. #}
list_reduce(
    list_transform(
        string_split(trim(cast({{ expr }} as varchar)), ' '),
        x -> upper(x[1]) || lower(x[2:])
    ),
    (a, b) -> a || ' ' || b
)
{% endmacro %}
