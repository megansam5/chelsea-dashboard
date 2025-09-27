-- models/marts/mart_chelsea_overview.sql
with team_details as (
    select * from {{ ref('stg_chelsea_team_details') }}
),

premier_league_position as (
    select 
        position,
        points,
        played_games,
        won,
        draw,
        lost,
        goals_for,
        goals_against,
        goal_difference,
        form
    from {{ ref('stg_premier_league_standings') }}
    where team_name = 'Chelsea FC'
),

champions_league_position as (
    select 
        position,
        points,
        played_games,
        won,
        draw,
        lost,
        goals_for,
        goals_against,
        goal_difference,
        form
    from {{ ref('stg_champions_league_standings') }}
    where team_name = 'Chelsea FC'
)

select
    td.team_id,
    td.team_name,
    td.team_shortname,
    td.team_tla,
    td.team_crest,
    td.address,
    td.website,
    td.founded,
    td.club_colors,
    td.venue,
    td.coach_name,
    td.coach_nationality,
    td.coach_contract_start,
    td.coach_contract_until,
    plp.position as premier_league_position,
    plp.points as premier_league_points,
    plp.played_games as premier_league_played,
    plp.won as premier_league_won,
    plp.draw as premier_league_draw,
    plp.lost as premier_league_lost,
    plp.goals_for as premier_league_gf,
    plp.goals_against as premier_league_ga,
    plp.goal_difference as premier_league_gd,
    plp.form as premier_league_form,
    clp.position as champions_league_position,
    clp.points as champions_league_points,
    clp.played_games as champions_league_played,
    clp.won as champions_league_won,
    clp.draw as champions_league_draw,
    clp.lost as champions_league_lost,
    clp.goals_for as champions_league_gf,
    clp.goals_against as champions_league_ga,
    clp.goal_difference as champions_league_gd,
    clp.form as champions_league_form
from team_details td
left join premier_league_position plp on 1=1
left join champions_league_position clp on 1=1