-- Test: Ensure Chelsea goals logic is consistent
select *
from {{ ref('mart_chelsea_matches') }}
where chelsea_goals is not null
  and opponent_goals is not null
  and (
    (venue_type = 'Home' and home_team_name <> 'Chelsea FC')
    or (venue_type = 'Away' and away_team_name <> 'Chelsea FC')
  )
