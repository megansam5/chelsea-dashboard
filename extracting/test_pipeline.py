import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    """Set fake environment variables for all tests."""
    monkeypatch.setenv("API_URL", "https://fake.api/")
    monkeypatch.setenv("API_KEY", "testkey")
    monkeypatch.setenv("BUCKET_NAME", "test-bucket")


def test_run_full_cloud_pipeline_calls_all_functions():
    """Ensure the pipeline calls all ingestion, parsing, and DB steps."""
    with patch("pipeline.ingest_data_to_s3") as mock_ingest, \
         patch("pipeline.parse_matches_s3") as mock_parse_matches, \
         patch("pipeline.parse_team_details_s3") as mock_parse_team, \
         patch("pipeline.parse_league_details_s3") as mock_parse_league, \
         patch("pipeline.parse_comp_standings_s3") as mock_parse_standings, \
         patch("pipeline.insert_data_to_db_from_s3") as mock_insert:
        
        import pipeline
        pipeline.run_full_cloud_pipeline()

        assert mock_ingest.call_count == 4


        all_args = [args for args, _ in mock_ingest.call_args_list]
        assert any("v4/teams/61/matches/" in a[3] for a in all_args)

        mock_parse_matches.assert_called_once()
        mock_parse_team.assert_called_once()
        mock_parse_league.assert_called_once()

        assert mock_parse_standings.call_count == 2

        mock_insert.assert_called_once()


def test_lambda_handler_success(monkeypatch):
    """Lambda should return success on successful run."""
    import pipeline
    with patch("pipeline.run_full_cloud_pipeline") as mock_run:
        result = pipeline.lambda_handler({}, {})
        assert result["statusCode"] == 200
        assert "successfully" in result["body"].lower()
        mock_run.assert_called_once()


def test_lambda_handler_failure(monkeypatch):
    """Lambda should return 500 and include error message on failure."""
    import pipeline
    with patch("pipeline.run_full_cloud_pipeline", side_effect=Exception("boom")):
        result = pipeline.lambda_handler({}, {})
        assert result["statusCode"] == 500
        assert "boom" in result["body"]
