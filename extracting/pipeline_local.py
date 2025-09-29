"""File that holds the main lambda handler function for the Fox News scraper."""

from dotenv import load_dotenv
from os import environ as ENV
import os

from extract_data import ingest_data
from parse_data import parse_comp_standings, parse_league_details, parse_matches, parse_team_details
from load_data import insert_data_to_db

def run_full_local_pipeline():
    base_url = ENV['API_URL']
    api_key = ENV['API_KEY']
    bucket_name = ENV['BUCKET_NAME']
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files")
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv_files/")

    ingest_data(base_url, api_key, bucket_name, 'v4/teams/61/matches/', "json_files/ChelseaMatches.json")
    ingest_data(base_url, api_key, bucket_name, 'v4/teams/61', "json_files/ChelseaTeamDetails.json")
    ingest_data(base_url, api_key, bucket_name, 'v4/competitions/2021/standings', "json_files/PremierLeagueStandings.json")
    ingest_data(base_url, api_key, bucket_name, 'v4/competitions/2001/standings', "json_files/ChampionsLeagueStandings.json")

    parse_matches(json_path, csv_path)
    parse_team_details(json_path, csv_path)
    parse_league_details(json_path, csv_path)
    parse_comp_standings(json_path, csv_path, 'Champions')
    parse_comp_standings(json_path, csv_path, 'Premier')

    insert_data_to_db()



if __name__ == "__main__":

    load_dotenv()

    run_full_local_pipeline()