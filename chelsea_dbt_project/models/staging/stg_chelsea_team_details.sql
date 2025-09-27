-- models/staging/stg_chelsea_team_details.sql
with src as (
    select * from {{ source('raw','chelsea_team_details') }}
)

select
    team_id::int as team_id,
    team_name as team_name,
    team_shortname as team_shortname,
    team_tla as team_tla,
    team_crest as team_crest,
    address as address,
    website as website,
    founded::int as founded,
    club_colors as club_colors,
    venue as venue,
    coach_id::int as coach_id,
    coach_name as coach_name,
    coach_firstname as coach_firstname,
    coach_lastname as coach_lastname,
    coach_dob::date as coach_dob,
    coach_nationality as coach_nationality,
    coach_contract_start as coach_contract_start,
    coach_contract_until as coach_contract_until,
    area_id::int as area_id,
    area_name as area_name,
    area_code as area_code,
    area_flag as area_flag
from src
