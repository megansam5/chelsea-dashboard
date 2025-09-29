import boto3
import json
import collections
import pandas as pd
from dotenv import load_dotenv
from os import environ as ENV
from io import StringIO


def get_s3_client():
    """Create and return S3 client."""
    return boto3.client(
        service_name="s3",
        aws_access_key_id=ENV["AWS_ACCESS_KEY"],
        aws_secret_access_key=ENV["AWS_SECRET_KEY"]
    )


def download_json_from_s3(bucket_name: str, s3_key: str):
    """Download JSON data from S3."""
    s3_client = get_s3_client()
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        json_content = response['Body'].read().decode('utf-8')
        return json.loads(json_content)
    except Exception as e:
        print(f"Failed to download {s3_key} from S3: {e}")
        raise


def upload_dataframe_to_s3(df: pd.DataFrame, bucket_name: str, s3_filename: str):
    """Uploads the DataFrame as a CSV to an S3 bucket using in-memory storage."""
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3_client = get_s3_client()
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_filename,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
        print(f"CSV uploaded to S3 bucket '{bucket_name}' as '{s3_filename}'")
    except Exception as e:
        print(f"Failed to upload CSV to S3: {e}")
        raise


def parse_matches_s3(bucket_name):
    """Parse Chelsea matches from S3 JSON and upload CSV to S3."""
    col_names = ['AREA_NAME', 'COMPETITION_ID', 'COMPETITION_NAME', 'SEASON_ID', 'SEASON_STARTDATE', 'SEASON_ENDDATE', 'CURRENT_MATCHDAY',
                 'MATCH_ID', 'MATCH_DATE', 'STATUS', 'STAGE', 'COMP_GROUP', 'HOME_TEAM_NAME', 'HOME_TEAM_ID', 'HOME_TEAM_TLA', 'HOME_TEAM_CREST',
                 'AWAY_TEAM_NAME', 'AWAY_TEAM_ID', 'AWAY_TEAM_TLA', 'AWAY_TEAM_CREST', 'WINNER', 'DURATION', 'FULLTIME_AWAY', 'FULLTIME_HOME', 'HALFTIME_AWAY', 'HALFTIME_HOME',
                 'REFEREE_NAME', 'REFEREE_NATIONALITY']

    try:
        print("Processing ChelseaMatches.json from S3")
        col_json = download_json_from_s3(bucket_name, 'json_files/ChelseaMatches.json')
        row_col = []

        for match in col_json.get('matches', []):
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

        # Convert to DataFrame and upload to S3
        df = pd.DataFrame(row_col, columns=col_names)
        upload_dataframe_to_s3(df, bucket_name, 'csv_files/ChelseaMatches.csv')

    except Exception as error:
        print(error)
        raise


def parse_team_details_s3(bucket_name):
    """Parse Chelsea team details from S3 JSON and upload CSVs to S3."""
    col_names_team = [
        'AREA_ID', 'AREA_NAME', 'AREA_CODE', 'AREA_FLAG',
        'TEAM_ID', 'TEAM_NAME', 'TEAM_SHORTNAME', 'TEAM_TLA', 'TEAM_CREST',
        'ADDRESS', 'WEBSITE', 'FOUNDED', 'CLUB_COLORS', 'VENUE',
        'COACH_ID', 'COACH_FIRSTNAME', 'COACH_LASTNAME', 'COACH_NAME',
        'COACH_DOB', 'COACH_NATIONALITY', 'COACH_CONTRACT_START', 'COACH_CONTRACT_UNTIL'
    ]

    col_names_players = ['PLAYER_ID', 'PLAYER_NAME', 'PLAYER_POSITION', 'PLAYER_DOB', 'PLAYER_NATIONALITY']

    try:
        print("Processing ChelseaTeamDetails.json from S3")
        player_data = download_json_from_s3(bucket_name, 'json_files/ChelseaTeamDetails.json')
        
        # Process team details
        row_col_team = []
        col_player = collections.OrderedDict()

        col_player['AREA_ID'] = player_data.get('area', {}).get('id')
        col_player['AREA_NAME'] = player_data.get('area', {}).get('name')
        col_player['AREA_CODE'] = player_data.get('area', {}).get('code')
        col_player['AREA_FLAG'] = player_data.get('area', {}).get('flag')

        col_player['TEAM_ID'] = player_data.get('id')
        col_player['TEAM_NAME'] = player_data.get('name')
        col_player['TEAM_SHORTNAME'] = player_data.get('shortName')
        col_player['TEAM_TLA'] = player_data.get('tla')
        col_player['TEAM_CREST'] = player_data.get('crest')

        col_player['ADDRESS'] = player_data.get('address')
        col_player['WEBSITE'] = player_data.get('website')
        col_player['FOUNDED'] = player_data.get('founded')
        col_player['CLUB_COLORS'] = player_data.get('clubColors')
        col_player['VENUE'] = player_data.get('venue')

        col_player['COACH_ID'] = player_data.get('coach', {}).get('id')
        col_player['COACH_FIRSTNAME'] = player_data.get('coach', {}).get('firstName')
        col_player['COACH_LASTNAME'] = player_data.get('coach', {}).get('lastName')
        col_player['COACH_NAME'] = player_data.get('coach', {}).get('name')
        col_player['COACH_DOB'] = player_data.get('coach', {}).get('dateOfBirth')
        col_player['COACH_NATIONALITY'] = player_data.get('coach', {}).get('nationality')
        col_player['COACH_CONTRACT_START'] = player_data.get('coach', {}).get('contract', {}).get('start')
        col_player['COACH_CONTRACT_UNTIL'] = player_data.get('coach', {}).get('contract', {}).get('until')

        row_col_team.append(col_player)

        # Convert team data to DataFrame and upload
        df_team = pd.DataFrame(row_col_team, columns=col_names_team)
        upload_dataframe_to_s3(df_team, bucket_name, 'csv_files/ChelseaTeamDetails.csv')

        # Process players
        row_col_player = []
        for player in player_data.get('squad', []):
            col_player = collections.OrderedDict()

            col_player['PLAYER_ID'] = player.get('id')
            col_player['PLAYER_NAME'] = player.get('name')
            col_player['PLAYER_POSITION'] = player.get('position')
            col_player['PLAYER_DOB'] = player.get('dateOfBirth')
            col_player['PLAYER_NATIONALITY'] = player.get('nationality')

            row_col_player.append(col_player)

        # Convert players data to DataFrame and upload
        df_players = pd.DataFrame(row_col_player, columns=col_names_players)
        upload_dataframe_to_s3(df_players, bucket_name, 'csv_files/ChelseaPlayers.csv')

    except Exception as error:
        print(error)
        raise


def parse_league_details_s3(bucket_name):
    """Parse league standings details from S3 and upload CSV to S3."""
    col_names = [
        'SEASON',
        'AREA_ID', 'AREA_NAME', 'AREA_CODE', 'AREA_FLAG',
        'COMPETITION_ID', 'COMPETITION_NAME', 'COMPETITION_CODE', 'COMPETITION_TYPE', 'COMPETITION_EMBLEM',
        'SEASON_ID', 'SEASON_STARTDATE', 'SEASON_ENDDATE', 'CURRENT_MATCHDAY', 'SEASON_WiNNER',
        'STAGE', 'STANDINGS_TYPE', 'COMP_GROUP'
    ]

    s3_client = get_s3_client()
    row_col = []
    
    try:
        # List all JSON files in the json_files/ prefix that end with 'Standings.json'
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='json_files/')
        
        for obj in response.get('Contents', []):
            file_key = obj['Key']
            if file_key.endswith('Standings.json'):
                print(f"Processing file {file_key}")
                
                competition_data = download_json_from_s3(bucket_name, file_key)
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

                # Standings is a list, so we'll pull the first one (if exists)
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

        # Convert to DataFrame and upload
        df = pd.DataFrame(row_col, columns=col_names)
        upload_dataframe_to_s3(df, bucket_name, 'csv_files/CompetitionDetails.csv')

    except Exception as error:
        print(error)
        raise


def parse_comp_standings_s3(bucket_name, league):
    """Parse competition standings from S3 and upload CSV to S3."""
    col_names = [
        'POSITION',
        'TEAM_ID', 'TEAM_NAME', 'TEAM_SHORTNAME', 'TEAM_TLA', 'TEAM_CREST',
        'PLAYED_GAMES', 'FORM', 'WON', 'DRAW', 'LOST',
        'POINTS', 'GOALS_FOR', 'GOALS_AGAINST', 'GOAL_DIFFERENCE'
    ]

    s3_json_key = f'json_files/{league}LeagueStandings.json'

    try:
        print(f"Processing {s3_json_key}")
        col_json = download_json_from_s3(bucket_name, s3_json_key)
        row_col = []

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

        # Convert to DataFrame and upload
        df = pd.DataFrame(row_col, columns=col_names)
        s3_csv_key = f'csv_files/{league}LeagueStandings.csv'
        upload_dataframe_to_s3(df, bucket_name, s3_csv_key)

    except Exception as error:
        print(error)
        raise


if __name__ == '__main__':
    load_dotenv()
    bucket_name = ENV['BUCKET_NAME']

    parse_matches_s3(bucket_name)
    parse_team_details_s3(bucket_name)
    parse_league_details_s3(bucket_name)
    parse_comp_standings_s3(bucket_name, 'Champions')
    parse_comp_standings_s3(bucket_name, 'Premier')