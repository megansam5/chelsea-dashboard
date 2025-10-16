import json
import os
import builtins
import pytest
from unittest.mock import patch, MagicMock
import collections
import parse_data


@pytest.fixture
def fake_paths(tmp_path):
    """Creates fake JSON and CSV directories."""
    json_dir = tmp_path / "json_files"
    csv_dir = tmp_path / "csv_files"
    json_dir.mkdir()
    csv_dir.mkdir()
    return str(json_dir), str(csv_dir)



def test_parse_matches_calls_writeData2CSV(fake_paths):
    """Verifies that JSON for matches is parsed and converted to a CSV."""
    json_path, csv_path = fake_paths
    data = {
        "matches": [
            {
                "area": {"name": "England"},
                "competition": {"id": 123, "name": "Premier League"},
                "season": {"id": 5, "startDate": "2024-01-01", "endDate": "2024-12-31", "currentMatchday": 8},
                "id": 555,
                "utcDate": "2024-10-10",
                "status": "FINISHED",
                "stage": "REGULAR_SEASON",
                "group": "A",
                "homeTeam": {"name": "Chelsea", "id": 1, "tla": "CHE", "crest": "crest1"},
                "awayTeam": {"name": "Arsenal", "id": 2, "tla": "ARS", "crest": "crest2"},
                "score": {
                    "winner": "HOME_TEAM",
                    "duration": "REGULAR",
                    "fullTime": {"home": 2, "away": 1},
                    "halfTime": {"home": 1, "away": 1},
                },
                "referees": [{"name": "Ref A", "nationality": "English"}],
            }
        ]
    }
    json_file = os.path.join(json_path, "ChelseaMatches.json")
    with open(json_file, "w") as f:
        json.dump(data, f)

    with patch("parse_data.writeData2CSV") as mock_write:
        parse_data.parse_matches(json_path, csv_path)

    mock_write.assert_called_once()
    args, kwargs = mock_write.call_args
    assert kwargs["file_name"] == "ChelseaMatches.csv"
    assert kwargs["writePath"] == csv_path
    assert len(kwargs["row_data"]) == 1
    assert kwargs["row_data"][0]["HOME_TEAM_NAME"] == "Chelsea"


def test_parse_team_details_calls_writeData2CSV(fake_paths):
    '''Ensures both team details and player lists are written out as separate CSVs.'''
    json_path, csv_path = fake_paths
    team_data = {
        "area": {"id": 10, "name": "England", "code": "ENG", "flag": "flag"},
        "id": 100,
        "name": "Chelsea",
        "shortName": "CFC",
        "tla": "CHE",
        "crest": "crest.png",
        "address": "London",
        "website": "chelsea.com",
        "founded": 1905,
        "clubColors": "Blue/White",
        "venue": "Stamford Bridge",
        "coach": {
            "id": 1,
            "firstName": "Mauricio",
            "lastName": "Pochettino",
            "name": "Mauricio Pochettino",
            "dateOfBirth": "1972-03-02",
            "nationality": "Argentina",
            "contract": {"start": "2023-01-01", "until": "2025-06-30"},
        },
        "squad": [
            {"id": 10, "name": "Player A", "position": "Forward", "dateOfBirth": "2000-01-01", "nationality": "English"},
            {"id": 11, "name": "Player B", "position": "Midfielder", "dateOfBirth": "1998-05-10", "nationality": "French"},
        ],
    }
    json_file = os.path.join(json_path, "ChelseaTeamDetails.json")
    with open(json_file, "w") as f:
        json.dump(team_data, f)

    with patch("parse_data.writeData2CSV") as mock_write:
        parse_data.parse_team_details(json_path, csv_path)

    assert mock_write.call_count == 2
    called_files = [c.kwargs["file_name"] for c in mock_write.call_args_list]
    assert "ChelseaTeamDetails.csv" in called_files
    assert "ChelseaPlayers.csv" in called_files



def test_parse_league_details(fake_paths):
    '''Confirms that league standings JSON produces a CompetitionDetails CSV.'''
    json_path, csv_path = fake_paths
    file = os.path.join(json_path, "PremierLeagueStandings.json")
    competition_data = {
        "filters": {"season": "2024"},
        "area": {"id": 1, "name": "England", "code": "ENG", "flag": "flag"},
        "competition": {"id": 39, "name": "Premier League", "code": "PL", "type": "LEAGUE", "emblem": "emblem"},
        "season": {"id": 5, "startDate": "2024-01-01", "endDate": "2024-12-31", "currentMatchday": 10, "winner": None},
        "standings": [{"stage": "REGULAR_SEASON", "type": "TOTAL", "group": None}],
    }
    with open(file, "w") as f:
        json.dump(competition_data, f)

    with patch("parse_data.writeData2CSV") as mock_write:
        parse_data.parse_league_details(json_path, csv_path)

    mock_write.assert_called_once()
    args, kwargs = mock_write.call_args
    assert kwargs["file_name"] == "CompetitionDetails.csv"
    assert len(kwargs["row_data"]) == 1
    assert kwargs["row_data"][0]["COMPETITION_NAME"] == "Premier League"



def test_parse_comp_standings(fake_paths):
    '''Checks that competition standings (like Champions League) generate the correct CSV file.'''
    json_path, csv_path = fake_paths
    league = "Premier"
    data = {
        "standings": [
            {
                "table": [
                    {
                        "position": 1,
                        "team": {"id": 1, "name": "Chelsea", "shortName": "CFC", "tla": "CHE", "crest": "crest"},
                        "playedGames": 10,
                        "form": "WDLWW",
                        "won": 6,
                        "draw": 2,
                        "lost": 2,
                        "points": 20,
                        "goalsFor": 18,
                        "goalsAgainst": 10,
                        "goalDifference": 8,
                    }
                ]
            }
        ]
    }
    json_file = os.path.join(json_path, f"{league}LeagueStandings.json")
    with open(json_file, "w") as f:
        json.dump(data, f)

    with patch("parse_data.writeData2CSV") as mock_write:
        parse_data.parse_comp_standings(json_path, csv_path, league)

    mock_write.assert_called_once()
    args, kwargs = mock_write.call_args
    assert kwargs["file_name"] == f"{league}LeagueStandings.csv"
    assert len(kwargs["row_data"]) == 1
    assert kwargs["row_data"][0]["TEAM_NAME"] == "Chelsea"
