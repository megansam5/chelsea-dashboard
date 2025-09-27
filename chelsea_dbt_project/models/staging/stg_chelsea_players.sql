-- models/staging/stg_chelsea_players.sql
with src as (
    select * from {{ source('raw','chelsea_players') }}
)

select
    player_id::int as player_id,
    player_name as player_name,
    player_position as position,
    player_dob::date as dob,
    player_nationality as nationality
from src
