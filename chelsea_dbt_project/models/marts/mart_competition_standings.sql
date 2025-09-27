-- models/marts/mart_competition_standings.sql
with premier_league as (
    select 
        'Premier League' as competition,
        position,
        team_id,
        team_name,
        team_shortname,
        team_tla,
        team_crest,
        played_games,
        form,
        won,
        draw,
        lost,
        points,
        goals_for,
        goals_against,
        goal_difference
    from {{ ref('stg_premier_league_standings') }}
),

champions_league as (
    select 
        'Champions League' as competition,
        position,
        team_id,
        team_name,
        team_shortname,
        team_tla,
        team_crest,
        played_games,
        form,
        won,
        draw,
        lost,
        points,
        goals_for,
        goals_against,
        goal_difference
    from {{ ref('stg_champions_league_standings') }}
),

combined_standings as (
    select * from premier_league
    union all
    select * from champions_league
)

select * from combined_standings
order by competition, position
