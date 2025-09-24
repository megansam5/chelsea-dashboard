import os
import json
import collections
from helperFunction import writeData2CSV

json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files/")
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv_files/")


def parse_matches(json_path, csv_path):

    col_names = ['AREA_NAME', 'COMPETITION_ID', 'COMPETITION_NAME', 'SEASON_ID', 'SEASON_STARTDATE', 'SEASON_ENDDATE', 'CURRENT_MATCHDAY',
                       'MATCH_ID', 'MATCH_DATE', 'STATUS', 'STAGE', 'COMP_GROUP', 'HOME_TEAM_NAME', 'HOME_TEAM_ID', 'HOME_TEAM_TLA', 'HOME_TEAM_CREST',
                 'AWAY_TEAM_NAME', 'AWAY_TEAM_ID', 'AWAY_TEAM_TLA', 'AWAY_TEAM_CREST', 'WINNER', 'DURATION', 'FULLTIME_AWAY', 'FULLTIME_HOME', 'HALFTIME_AWAY', 'HALFTIME_HOME',
                 'REFEREE_NAME', 'REFEREE_NATIONALITY']

    read_path = os.path.join(json_path, 'ChelseaMatches.json')

    try:
        with open(read_path, mode='r', encoding='utf-8') as f:
            print("Processing file ", read_path)
            row_col = []

            json_f = f.read()
            col_json = json.loads(json_f)

            for match in col_json.get('matches'):

                col_match = collections.OrderedDict()

                col_match['AREA_NAME'] = match.get('area', {}).get('name')
                col_match['COMPETITION_ID'] = match.get('competition', {}).get('id')
                col_match['COMPETITION_NAME'] = match.get('competition', {}).get('name')
                col_match['SEASON_ID'] = match.get('season', {}).get('id')
                col_match['SEASON_STARTDATE'] = match.get('season', {}).get('startDate')
                col_match['SEASON_ENDDATE'] = match.get('season', {}).get('endDate')
                col_match['CURRENT_MATCHDAY'] = match.get('season', {}).get('currentMatchday')

                col_match['MATCH_ID'] = match.get('id')
                col_match['MATCH_DATE'] = match.get('utcDate')
                col_match['STATUS'] = match.get('status')
                col_match['STAGE'] = match.get('stage')
                col_match['COMP_GROUP'] = match.get('group')

                col_match['HOME_TEAM_NAME'] = match.get('homeTeam', {}).get('name')
                col_match['HOME_TEAM_ID'] = match.get('homeTeam', {}).get('id')
                col_match['HOME_TEAM_TLA'] = match.get('homeTeam', {}).get('tla')
                col_match['HOME_TEAM_CREST'] = match.get('homeTeam', {}).get('crest')

                col_match['AWAY_TEAM_NAME'] = match.get('awayTeam', {}).get('name')
                col_match['AWAY_TEAM_ID'] = match.get('awayTeam', {}).get('id')
                col_match['AWAY_TEAM_TLA'] = match.get('awayTeam', {}).get('tla')
                col_match['AWAY_TEAM_CREST'] = match.get('awayTeam', {}).get('crest')

                col_match['WINNER'] = match.get('score', {}).get('winner')
                col_match['DURATION'] = match.get('score', {}).get('duration')
                col_match['FULLTIME_AWAY'] = match.get('score', {}).get('fullTime', {}).get('away')
                col_match['FULLTIME_HOME'] = match.get('score', {}).get('fullTime', {}).get('home')
                col_match['HALFTIME_AWAY'] = match.get('score', {}).get('halfTime', {}).get('away')
                col_match['HALFTIME_HOME'] = match.get('score', {}).get('halfTime', {}).get('home')

                # Referees is a list — assume we want the first referee if present
                referees = match.get('referees', [])
                if referees:
                    col_match['REFEREE_NAME'] = referees[0].get('name')
                    col_match['REFEREE_NATIONALITY'] = referees[0].get('nationality')
                else:
                    col_match['REFEREE_NAME'] = None
                    col_match['REFEREE_NATIONALITY'] = None

                row_col.append(col_match)

        writeData2CSV(file_name='ChelseaMatches.csv',
                      writePath=csv_path, col_names=col_names, row_data=row_col)



    except Exception as error:
        print(error)
        raise

def parse_team_details(json_path, csv_path):
    col_names_team = [
        'AREA_ID', 'AREA_NAME', 'AREA_CODE', 'AREA_FLAG',
        'TEAM_ID', 'TEAM_NAME', 'TEAM_SHORTNAME', 'TEAM_TLA', 'TEAM_CREST',
        'ADDRESS', 'WEBSITE', 'FOUNDED', 'CLUB_COLORS', 'VENUE',
        'COACH_ID', 'COACH_FIRSTNAME', 'COACH_LASTNAME', 'COACH_NAME',
        'COACH_DOB', 'COACH_NATIONALITY', 'COACH_CONTRACT_START', 'COACH_CONTRACT_UNTIL'
    ]

    col_names_players = ['PLAYER_ID', 'PLAYER_NAME', 'PLAYER_POSITION', 'PLAYER_DOB', 'PLAYER_NATIONALITY']

    read_path = os.path.join(json_path, 'ChelseaTeamDetails.json')


    try:
        with open(read_path, mode='r', encoding='utf-8') as f:
            print("Processing file ", read_path)
            row_col_team = []

            json_f = f.read()
            player = json.loads(json_f)



            col_player = collections.OrderedDict()

            col_player['AREA_ID'] = player.get('area', {}).get('id')
            col_player['AREA_NAME'] = player.get('area', {}).get('name')
            col_player['AREA_CODE'] = player.get('area', {}).get('code')
            col_player['AREA_FLAG'] = player.get('area', {}).get('flag')

            col_player['TEAM_ID'] = player.get('id')
            col_player['TEAM_NAME'] = player.get('name')
            col_player['TEAM_SHORTNAME'] = player.get('shortName')
            col_player['TEAM_TLA'] = player.get('tla')
            col_player['TEAM_CREST'] = player.get('crest')

            col_player['ADDRESS'] = player.get('address')
            col_player['WEBSITE'] = player.get('website')
            col_player['FOUNDED'] = player.get('founded')
            col_player['CLUB_COLORS'] = player.get('clubColors')
            col_player['VENUE'] = player.get('venue')

            col_player['COACH_ID'] = player.get('coach', {}).get('id')
            col_player['COACH_FIRSTNAME'] = player.get('coach', {}).get('firstName')
            col_player['COACH_LASTNAME'] = player.get('coach', {}).get('lastName')
            col_player['COACH_NAME'] = player.get('coach', {}).get('name')
            col_player['COACH_DOB'] = player.get('coach', {}).get('dateOfBirth')
            col_player['COACH_NATIONALITY'] = player.get('coach', {}).get('nationality')
            col_player['COACH_CONTRACT_START'] = player.get('coach', {}).get('contract', {}).get('start')
            col_player['COACH_CONTRACT_UNTIL'] = player.get('coach', {}).get('contract', {}).get('until')

            row_col_team.append(col_player)

        writeData2CSV(file_name='ChelseaTeamDetails.csv',
                      writePath=csv_path, col_names=col_names_team, row_data=row_col_team)

        with open(read_path, mode='r', encoding='utf-8') as f:
            print("Processing file ", read_path)
            row_col_player = []

            json_f = f.read()
            col_json = json.loads(json_f)
            for player in col_json.get('squad'):

                col_player = collections.OrderedDict()

                col_player['PLAYER_ID'] = player.get('id')
                col_player['PLAYER_NAME'] = player.get('name')
                col_player['PLAYER_POSITION'] = player.get('position')
                col_player['PLAYER_DOB'] = player.get('dateOfBirth')
                col_player['PLAYER_NATIONALITY'] = player.get('nationality')

                row_col_player.append(col_player)

        writeData2CSV(file_name='ChelseaPlayers.csv',
                      writePath=csv_path, col_names=col_names_players, row_data=row_col_player)

    except Exception as error:
        print(error)
        raise


def parse_league_details(json_path, csv_path):
    col_names = [
        'SEASON',
        'AREA_ID', 'AREA_NAME', 'AREA_CODE', 'AREA_FLAG',
        'COMPETITION_ID', 'COMPETITION_NAME', 'COMPETITION_CODE', 'COMPETITION_TYPE', 'COMPETITION_EMBLEM',
        'SEASON_ID', 'SEASON_STARTDATE', 'SEASON_ENDDATE', 'CURRENT_MATCHDAY', 'SEASON_WiNNER',
        'STAGE', 'STANDINGS_TYPE', 'COMP_GROUP'
    ]

    file_suffix = 'Standings.json'
    row_col = []
    try:
        for file in os.listdir(json_path):
            if file.endswith(file_suffix):
                read_path = os.path.join(json_path, file)

                with open(read_path, mode='r', encoding='utf-8') as f:
                    print("Processing file ", read_path)

                    json_f = f.read()
                    competition_data = json.loads(json_f)

                    col_competition = collections.OrderedDict()

                    col_competition['SEASON'] = competition_data.get('filters', {}).get('season')

                    col_competition['AREA_ID'] = competition_data.get('area', {}).get('id')
                    col_competition['AREA_NAME'] = competition_data.get('area', {}).get('name')
                    col_competition['AREA_CODE'] = competition_data.get('area', {}).get('code')
                    col_competition['AREA_FLAG'] = competition_data.get('area', {}).get('flag')

                    col_competition['COMPETITION_ID'] = competition_data.get('competition', {}).get('id')
                    col_competition['COMPETITION_NAME'] = competition_data.get('competition', {}).get('name')
                    col_competition['COMPETITION_CODE'] = competition_data.get('competition', {}).get('code')
                    col_competition['COMPETITION_TYPE'] = competition_data.get('competition', {}).get('type')
                    col_competition['COMPETITION_EMBLEM'] = competition_data.get('competition', {}).get('emblem')

                    col_competition['SEASON_ID'] = competition_data.get('season', {}).get('id')
                    col_competition['SEASON_STARTDATE'] = competition_data.get('season', {}).get('startDate')
                    col_competition['SEASON_ENDDATE'] = competition_data.get('season', {}).get('endDate')
                    col_competition['CURRENT_MATCHDAY'] = competition_data.get('season', {}).get('currentMatchday')
                    col_competition['SEASON_WiNNER'] = competition_data.get('season', {}).get('winner')

                    # Standings is a list, so we’ll pull the first one (if exists)
                    standings = competition_data.get('standings', [])
                    if standings:
                        col_competition['STAGE'] = standings[0].get('stage')
                        col_competition['STANDINGS_TYPE'] = standings[0].get('type')
                        col_competition['COMP_GROUP'] = standings[0].get('group')
                    else:
                        col_competition['STAGE'] = None
                        col_competition['STANDINGS_TYPE'] = None
                        col_competition['COMP_GROUP'] = None

                    row_col.append(col_competition)

        writeData2CSV(file_name='CompetitionDetails.csv',
                      writePath=csv_path, col_names=col_names, row_data=row_col)

    except Exception as error:
        print(error)
        raise

def parse_comp_standings(json_path, csv_path, league):
    col_names = [
        'POSITION',
        'TEAM_ID', 'TEAM_NAME', 'TEAM_SHORTNAME', 'TEAM_TLA', 'TEAM_CREST',
        'PLAYED_GAMES', 'FORM', 'WON', 'DRAW', 'LOST',
        'POINTS', 'GOALS_FOR', 'GOALS_AGAINST', 'GOAL_DIFFERENCE'
    ]

    in_file_name = league + 'LeagueStandings.json'

    read_path = os.path.join(json_path, in_file_name)


    try:

        with open(read_path, mode='r', encoding='utf-8') as f:
            print("Processing file ", read_path)
            row_col = []

            json_f = f.read()
            col_json = json.loads(json_f)

            standings = col_json.get('standings', [])
            if standings:
                table = standings[0].get('table')
                for standing in table:
                    col_standing = collections.OrderedDict()

                    col_standing['POSITION'] = standing.get('position')

                    col_standing['TEAM_ID'] = standing.get('team', {}).get('id')
                    col_standing['TEAM_NAME'] = standing.get('team', {}).get('name')
                    col_standing['TEAM_SHORTNAME'] = standing.get('team', {}).get('shortName')
                    col_standing['TEAM_TLA'] = standing.get('team', {}).get('tla')
                    col_standing['TEAM_CREST'] = standing.get('team', {}).get('crest')

                    col_standing['PLAYED_GAMES'] = standing.get('playedGames')
                    col_standing['FORM'] = standing.get('form')
                    col_standing['WON'] = standing.get('won')
                    col_standing['DRAW'] = standing.get('draw')
                    col_standing['LOST'] = standing.get('lost')

                    col_standing['POINTS'] = standing.get('points')
                    col_standing['GOALS_FOR'] = standing.get('goalsFor')
                    col_standing['GOALS_AGAINST'] = standing.get('goalsAgainst')
                    col_standing['GOAL_DIFFERENCE'] = standing.get('goalDifference')

                    row_col.append(col_standing)

        file_name = league + 'LeagueStandings.csv'
        writeData2CSV(file_name=file_name,
                      writePath=csv_path, col_names=col_names, row_data=row_col)

    except Exception as error:
        print(error)
        raise

if __name__ == '__main__':
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files/")
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv_files/")

    parse_matches(json_path, csv_path)
    parse_team_details(json_path, csv_path)
    parse_league_details(json_path, csv_path)
    parse_comp_standings(json_path, csv_path, 'Champions')
    parse_comp_standings(json_path, csv_path, 'Premier')