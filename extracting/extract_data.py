from helperFunction import wrappedRequest
from dotenv import load_dotenv
from os import environ as ENV
import os
import json
import boto3
from io import StringIO


def ingest_data(url, key, path, api_name, f_name):
    parameters={}
    headers={}
    headers['X-Auth-Token'] = key
    full_url = url + api_name
    file_name = os.path.join(path, f_name)
    try:
        result = wrappedRequest(full_url, params=parameters, headers=headers)
        r = result.get('result')

        print("Response Code = {}, requested URL {}".format(r.status_code, r.url))
        json_data = json.loads(r.text)
        with open(file_name, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(json_data))
        print("Downloaded data in file {}".format(file_name))
    except Exception as error:
        print(error)
        raise

def upload_json_to_s3(json_data: dict, bucket_name: str, s3_filename: str):
    """Uploads JSON data to S3 bucket using in-memory storage."""
    json_buffer = StringIO()
    json.dump(json_data, json_buffer, indent=2)
    
    s3_client = boto3.client(
        service_name="s3",
        aws_access_key_id=ENV["AWS_ACCESS_KEY"],
        aws_secret_access_key=ENV["AWS_SECRET_KEY"]
    )
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_filename,
            Body=json_buffer.getvalue(),
            ContentType='application/json'
        )
        print(f"JSON file uploaded to S3 bucket '{bucket_name}' as '{s3_filename}'")
    except Exception as e:
        print(f"Failed to upload JSON file to S3: {e}")
        raise


def ingest_data_to_s3(url, key, bucket_name, api_name, s3_filename):
    """Extract data from API and upload directly to S3."""
    parameters = {}
    headers = {}
    headers['X-Auth-Token'] = key
    full_url = url + api_name
    
    try:
        result = wrappedRequest(full_url, params=parameters, headers=headers)
        r = result.get('result')
        
        print("Response Code = {}, requested URL {}".format(r.status_code, r.url))
        json_data = json.loads(r.text)
        
        # Upload directly to S3
        upload_json_to_s3(json_data, bucket_name, s3_filename)
        print("Data uploaded to S3 as {}".format(s3_filename))
        
    except Exception as error:
        print(error)
        raise

if __name__ == '__main__':
    load_dotenv()
    base_url = ENV['API_URL']
    api_key = ENV['API_KEY']
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files")

    ingest_data(base_url, api_key, json_path, 'v4/teams/61/matches/', "ChelseaMatches.json")
    ingest_data(base_url, api_key, json_path, 'v4/teams/61', "ChelseaTeamDetails.json")
    ingest_data(base_url, api_key, json_path, 'v4/competitions/2021/standings', "PremierLeagueStandings.json")
    ingest_data(base_url, api_key, json_path, 'v4/competitions/2001/standings', "ChampionsLeagueStandings.json")