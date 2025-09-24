from helperFunction import wrappedRequest
from dotenv import load_dotenv
from os import environ as ENV
import os
import json


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

if __name__ == '__main__':
    load_dotenv()
    base_url = ENV['API_URL']
    api_key = ENV['API_KEY']
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files")

    ingest_data(base_url, api_key, json_path, 'v4/teams/61/matches/', "ChelseaMatches.json")
    ingest_data(base_url, api_key, json_path, 'v4/teams/61', "ChelseaTeamDetails.json")
    ingest_data(base_url, api_key, json_path, 'v4/competitions/2021/standings', "PremierLeagueStandings.json")
    ingest_data(base_url, api_key, json_path, 'v4/competitions/2001/standings', "ChampionsLeagueStandings.json")