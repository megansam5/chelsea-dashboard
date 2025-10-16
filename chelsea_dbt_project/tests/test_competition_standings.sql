-- Test: No duplicate team positions per competition
select competition, position, count(*)
from {{ ref('mart_competition_standings') }}
group by competition, position
having count(*) > 1
