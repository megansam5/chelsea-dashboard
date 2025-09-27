-- models/marts/mart_chelsea_players.sql

with players as (
    select * from {{ ref('stg_chelsea_players') }}
),
classified as (
    select
        player_id,
        player_name,
        position,
        dob,
        nationality,
        extract(year from age(current_date, dob)) as age,
        case 
            when position in ('Goalkeeper') then 'GK'
            when position in ('Centre-Back', 'Left-Back', 'Right-Back', 'Defender') then 'DEF'
            when position in ('Defensive Midfield', 'Central Midfield', 'Attacking Midfield', 'Left Midfield', 'Right Midfield', 'Midfielder') then 'MID'
            when position in ('Centre-Forward', 'Left Winger', 'Right Winger', 'Forward', 'Attacking Midfielder') then 'ATT'
            else 'UNKNOWN'
        end as position_category
    from players
)
select *
from classified
order by 
    case position_category
        when 'GK' then 1
        when 'DEF' then 2
        when 'MID' then 3
        when 'ATT' then 4
        else 5
    end,
    player_name