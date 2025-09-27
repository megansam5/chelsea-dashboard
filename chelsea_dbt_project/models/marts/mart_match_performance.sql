-- models/marts/mart_match_performance.sql
with match_results as (
    select * from {{ ref('mart_chelsea_matches') }}
    where status = 'FINISHED'
),

performance_stats as (
    select
        competition_name,
        count(*) as total_matches,
        sum(case when result = 'Win' then 1 else 0 end) as wins,
        sum(case when result = 'Draw' then 1 else 0 end) as draws,
        sum(case when result = 'Loss' then 1 else 0 end) as losses,
        sum(chelsea_goals) as goals_scored,
        sum(opponent_goals) as goals_conceded,
        sum(chelsea_goals) - sum(opponent_goals) as goal_difference,
        round(
            (sum(case when result = 'Win' then 3 when result = 'Draw' then 1 else 0 end) * 100.0) / 
            (count(*) * 3), 2
        ) as points_percentage
    from match_results
    group by competition_name
),

recent_form as (
    select
        competition_name,
        string_agg(
            case 
                when result = 'Win' then 'W'
                when result = 'Draw' then 'D'
                when result = 'Loss' then 'L'
            end, 
            '' order by match_date desc
        ) as last_5_form
    from (
        select 
            competition_name,
            match_date,
            result,
            row_number() over (partition by competition_name order by match_date desc) as rn
        from match_results
    ) last_matches
    where rn <= 5
    group by competition_name
)

select
    ps.*,
    rf.last_5_form
from performance_stats ps
left join recent_form rf on ps.competition_name = rf.competition_name