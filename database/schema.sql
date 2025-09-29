DROP TABLE IF EXISTS chelsea_matches;
DROP TABLE IF EXISTS chelsea_team_details;
DROP TABLE IF EXISTS chelsea_players;
DROP TABLE IF EXISTS competition_details;
DROP TABLE IF EXISTS premier_league_standings;
DROP TABLE IF EXISTS champions_league_standings;

CREATE TABLE chelsea_matches (
    area_name TEXT,
    competition_id INT,
    competition_name TEXT,
    season_id INT,
    season_startdate DATE,
    season_enddate DATE,
    current_matchday INT,
    match_id BIGINT PRIMARY KEY,
    match_date DATE,
    status TEXT,
    stage TEXT,
    comp_group TEXT,
    home_team_name TEXT,
    home_team_id INT,
    home_team_tla TEXT,
    home_team_crest TEXT,
    away_team_name TEXT,
    away_team_id INT,
    away_team_tla TEXT,
    away_team_crest TEXT,
    winner TEXT,
    duration TEXT,
    fulltime_away INT,
    fulltime_home INT,
    halftime_away INT,
    halftime_home INT,
    referee_name TEXT,
    referee_nationality TEXT
);

CREATE TABLE chelsea_team_details (
    area_id INT,
    area_name TEXT,
    area_code TEXT,
    area_flag TEXT,
    team_id INT PRIMARY KEY,
    team_name TEXT,
    team_shortname TEXT,
    team_tla TEXT,
    team_crest TEXT,
    address TEXT,
    website TEXT,
    founded INT,
    club_colors TEXT,
    venue TEXT,
    coach_id INT,
    coach_firstname TEXT,
    coach_lastname TEXT,
    coach_name TEXT,
    coach_dob DATE,
    coach_nationality TEXT,
    coach_contract_start TEXT,
    coach_contract_until TEXT
);

CREATE TABLE chelsea_players (
    player_id INT PRIMARY KEY,
    player_name TEXT,
    player_position TEXT,
    player_dob DATE,
    player_nationality TEXT
);


CREATE TABLE competition_details (
    season TEXT,
    area_id INT,
    area_name TEXT,
    area_code TEXT,
    area_flag TEXT,
    competition_id INT PRIMARY KEY,
    competition_name TEXT,
    competition_code TEXT,
    competition_type TEXT,
    competition_emblem TEXT,
    season_id INT,
    season_startdate DATE,
    season_enddate DATE,
    current_matchday INT,
    season_winner TEXT,
    stage TEXT,
    standings_type TEXT,
    comp_group TEXT
);


CREATE TABLE premier_league_standings (
    position INT,
    team_id INT,
    team_name TEXT,
    team_shortname TEXT,
    team_tla TEXT,
    team_crest TEXT,
    played_games INT,
    form TEXT,
    won INT,
    draw INT,
    lost INT,
    points INT,
    goals_for INT,
    goals_against INT,
    goal_difference INT,
    PRIMARY KEY (position, team_id)
);


CREATE TABLE champions_league_standings (
    position INT,
    team_id INT,
    team_name TEXT,
    team_shortname TEXT,
    team_tla TEXT,
    team_crest TEXT,
    played_games INT,
    form TEXT,
    won INT,
    draw INT,
    lost INT,
    points INT,
    goals_for INT,
    goals_against INT,
    goal_difference INT,
    PRIMARY KEY (position, team_id)
);