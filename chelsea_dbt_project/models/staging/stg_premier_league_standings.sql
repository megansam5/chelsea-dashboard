-- models/staging/stg_premier_league_standings.sql
with src as (
    select * from {{ source('raw','premier_league_standings') }}
)

select
    position::int as position,
    team_id::int as team_id,
    team_name as team_name,
    team_shortname as team_shortname,
    team_tla as team_tla,
    team_crest as team_crest,
    played_games::int as played_games,
    form as form,
    won::int as won,
    draw::int as draw,
    lost::int as lost,
    points::int as points,
    goals_for::int as goals_for,
    goals_against::int as goals_against,
    goal_difference::int as goal_difference
from src
