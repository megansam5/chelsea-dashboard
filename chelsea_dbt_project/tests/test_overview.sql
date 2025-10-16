-- Test: Only Chelsea FC should appear in overview
select *
from {{ ref('mart_chelsea_overview') }}
where team_name <> 'Chelsea FC'
