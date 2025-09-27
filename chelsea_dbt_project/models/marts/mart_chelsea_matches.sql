-- models/marts/mart_chelsea_matches.sql

with matches as (
    select * from {{ ref('stg_chelsea_matches') }}
),

enriched_matches as (
    select
        match_id,
        match_date,
        competition_name,
        season_startdate,
        season_enddate,
        current_matchday,
        status,
        stage,
        comp_group,
        home_team_name,
        home_team_tla,
        away_team_name,
        away_team_tla,
        case 
            when home_team_name = 'Chelsea FC' then 'Home'
            when away_team_name = 'Chelsea FC' then 'Away'
            else 'Unknown'
        end as venue_type,
        case 
            when home_team_name = 'Chelsea FC' then away_team_name
            when away_team_name = 'Chelsea FC' then home_team_name
            else 'Unknown'
        end as opponent,
        case 
            when home_team_name = 'Chelsea FC' then away_team_tla
            when away_team_name = 'Chelsea FC' then home_team_tla
            else 'Unknown'
        end as opponent_tla,
        winner,
        duration,
        fulltime_home,
        fulltime_away,
        case 
            when home_team_name = 'Chelsea FC' then fulltime_home
            when away_team_name = 'Chelsea FC' then fulltime_away
            else null
        end as chelsea_goals,
        case 
            when home_team_name = 'Chelsea FC' then fulltime_away
            when away_team_name = 'Chelsea FC' then fulltime_home
            else null
        end as opponent_goals,
        halftime_home,
        halftime_away,
        referee_name,
        referee_nationality,
        area_name,
        case
            when status = 'FINISHED' then
                case
                    when (home_team_name = 'Chelsea FC' and fulltime_home > fulltime_away) or
                         (away_team_name = 'Chelsea FC' and fulltime_away > fulltime_home) then 'Win'
                    when fulltime_home = fulltime_away then 'Draw'
                    else 'Loss'
                end
            else 'Not Played'
        end as result
    from matches
)

select * from enriched_matches
order by match_date desc

