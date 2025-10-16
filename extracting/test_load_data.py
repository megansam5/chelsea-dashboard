import os
import pytest
import pandas as pd
from io import StringIO
from unittest.mock import patch, MagicMock
from moto import mock_aws

import load_data


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Set required environment variables for all tests."""
    monkeypatch.setenv("AWS_ACCESS_KEY", "fake_access")
    monkeypatch.setenv("AWS_SECRET_KEY", "fake_secret")
    monkeypatch.setenv("DB_NAME", "fake_db")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_USER", "user")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_PASSWORD", "password")
    monkeypatch.setenv("BUCKET_NAME", "fake-bucket")


@mock_aws
def test_get_s3_client_returns_valid_client():
    client = load_data.get_s3_client()
    buckets = client.list_buckets()
    assert isinstance(buckets, dict), "Expected a valid boto3 S3 client response"


@patch("load_data.psycopg2.connect")
def test_connect_to_postgres_calls_psycopg2(mock_connect):
    """Ensure psycopg2.connect is called with correct parameters."""
    load_data.connect_to_postgres()
    mock_connect.assert_called_once()
    args, kwargs = mock_connect.call_args
    assert kwargs["dbname"] == "fake_db"
    assert kwargs["host"] == "localhost"
    assert kwargs["user"] == "user"
    assert kwargs["port"] == "5432"
    assert kwargs["password"] == "password"


@mock_aws
def test_download_csv_from_s3_to_dataframe(monkeypatch):
    """Test successful download of CSV from mock S3."""
    import boto3
    s3 = boto3.client("s3")
    bucket_name = "fake-bucket"
    s3.create_bucket(Bucket=bucket_name)

    csv_data = "col1,col2\n1,2\n3,4\n"
    s3.put_object(Bucket=bucket_name, Key="data.csv", Body=csv_data)

    df = load_data.download_csv_from_s3_to_dataframe(bucket_name, "data.csv")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["col1", "col2"]
    assert len(df) == 2


@mock_aws
def test_download_csv_from_s3_to_dataframe_raises(monkeypatch):
    """Test exception handling when S3 get_object fails."""
    monkeypatch.setattr("load_data.get_s3_client", lambda: MagicMock(
        get_object=MagicMock(side_effect=Exception("S3 error"))
    ))
    with pytest.raises(Exception, match="S3 error"):
        load_data.download_csv_from_s3_to_dataframe("bucket", "missing.csv")


def test_insert_dataframe_to_postgres_executes_queries(monkeypatch):
    """Test that insert_dataframe_to_postgres truncates and loads data."""
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    load_data.insert_dataframe_to_postgres(df, "test_table", mock_conn)

    mock_cursor.execute.assert_any_call("TRUNCATE TABLE test_table;")
    assert mock_cursor.copy_from.called, "Should use COPY FROM to load data"



@patch("load_data.connect_to_postgres")
def test_insert_data_to_db_loads_all_csvs(mock_connect, tmp_path, monkeypatch):
    """Test that insert_data_to_db truncates and loads each table."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor


    csv_dir = tmp_path / "csv_files"
    csv_dir.mkdir()
    for name in [
        "ChampionsLeagueStandings.csv",
        "PremierLeagueStandings.csv",
        "ChelseaMatches.csv",
        "ChelseaPlayers.csv",
        "CompetitionDetails.csv",
        "ChelseaTeamDetails.csv",
    ]:
        (csv_dir / name).write_text("col1,col2\n1,2\n")


    monkeypatch.setattr(load_data, "__file__", str(tmp_path / "load_data.py"))


    import builtins
    real_open = builtins.open

    with patch("builtins.open", side_effect=lambda f, *a, **k: real_open(f, *a, **k)):
        load_data.insert_data_to_db()

    assert mock_cursor.execute.call_count >= 6
    assert mock_cursor.copy_from.call_count >= 6
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()



@patch("load_data.connect_to_postgres")
def test_insert_data_to_db_from_s3_success(mock_connect):
    """Test S3-to-Postgres data flow succeeds."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    fake_df = pd.DataFrame({"col1": [1, 2]})
    with patch("load_data.download_csv_from_s3_to_dataframe", return_value=fake_df), \
         patch("load_data.insert_dataframe_to_postgres") as mock_insert:
        load_data.insert_data_to_db_from_s3()

    mock_insert.assert_called()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("load_data.connect_to_postgres")
def test_insert_data_to_db_from_s3_rollback_on_error(mock_connect):
    """Test rollback when an error occurs in insert_data_to_db_from_s3."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch("load_data.download_csv_from_s3_to_dataframe", side_effect=Exception("Bad S3")):
        with pytest.raises(Exception, match="Bad S3"):
            load_data.insert_data_to_db_from_s3()

    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
