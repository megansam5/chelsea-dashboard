-- models/staging/stg_competition_details.sql
with src as (
    select * from {{ source('raw','competition_details') }}
)

select
    competition_id::int as competition_id,
    competition_name as competition_name,
    competition_code as competition_code,
    competition_type as competition_type,
    competition_emblem as competition_emblem,
    season as season,
    season_id::int as season_id,
    season_startdate::date as season_startdate,
    season_enddate::date as season_enddate,
    current_matchday::int as current_matchday,
    season_winner as season_winner,
    area_id::int as area_id,
    area_name as area_name,
    area_code as area_code,
    area_flag as area_flag,
    stage as stage,
    standings_type as standings_type,
    comp_group as comp_group
from src
