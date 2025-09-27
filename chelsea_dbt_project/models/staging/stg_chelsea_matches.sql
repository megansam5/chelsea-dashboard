-- models/staging/stg_chelsea_matches.sql
with src as (
    select * from {{ source('raw','chelsea_matches') }}
)

select
    match_id::bigint as match_id,
    match_date::date as match_date,
    competition_id::int as competition_id,
    competition_name as competition_name,
    season_id::int as season_id,
    season_startdate::date as season_startdate,
    season_enddate::date as season_enddate,
    current_matchday::int as current_matchday,
    status as status,
    stage as stage,
    comp_group as comp_group,
    home_team_id::int as home_team_id,
    home_team_name as home_team_name,
    home_team_tla as home_team_tla,
    away_team_id::int as away_team_id,
    away_team_name as away_team_name,
    away_team_tla as away_team_tla,
    winner as winner,
    duration as duration,
    fulltime_home::int as fulltime_home,
    fulltime_away::int as fulltime_away,
    halftime_home::int as halftime_home,
    halftime_away::int as halftime_away,
    referee_name as referee_name,
    referee_nationality as referee_nationality,
    area_name as area_name
from src
