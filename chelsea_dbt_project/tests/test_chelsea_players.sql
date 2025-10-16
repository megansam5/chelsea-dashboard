-- Test: No players with negative or null age
select *
from {{ ref('mart_chelsea_players') }}
where age is null or age < 0
