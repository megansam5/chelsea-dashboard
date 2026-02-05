"""File that holds the main lambda handler function for the cloud pipeline."""

from dotenv import load_dotenv
from os import environ as ENV

from extract_data import ingest_data_to_s3
from parse_data_cloud import parse_comp_standings_s3, parse_league_details_s3, parse_matches_s3, parse_team_details_s3
from load_data import insert_data_to_db_from_s3

def run_full_cloud_pipeline():
    base_url = ENV['API_URL']
    api_key = ENV['API_KEY']
    bucket_name = ENV['BUCKET_NAME']
    ingest_data_to_s3(base_url, api_key, bucket_name, 'v4/teams/61/matches/', "json_files/ChelseaMatches.json")
    ingest_data_to_s3(base_url, api_key, bucket_name, 'v4/teams/61', "json_files/ChelseaTeamDetails.json")
    ingest_data_to_s3(base_url, api_key, bucket_name, 'v4/competitions/2021/standings', "json_files/PremierLeagueStandings.json")
    ingest_data_to_s3(base_url, api_key, bucket_name, 'v4/competitions/2001/standings', "json_files/ChampionsLeagueStandings.json")

    parse_matches_s3(bucket_name)
    parse_team_details_s3(bucket_name)
    parse_league_details_s3(bucket_name)
    parse_comp_standings_s3(bucket_name, 'Champions')
    parse_comp_standings_s3(bucket_name, 'Premier')

    insert_data_to_db_from_s3()


def lambda_handler(event, context):  # pylint: disable=W0613
    """AWS Lambda handler function."""

    try:
        run_full_cloud_pipeline()
        return {
            "statusCode": 200,
            "body": "RSS feed data processed and uploaded to S3 successfully."
        }

    except Exception as e:  # pylint: disable=W0718
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }


if __name__ == "__main__":

    load_dotenv()

    result = lambda_handler({}, {})
    print(result)