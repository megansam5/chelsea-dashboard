-- Test: Ensure calculated matches match sum of wins/draws/losses
select *
from {{ ref('mart_match_performance') }}
where total_matches <> (wins + draws + losses)
