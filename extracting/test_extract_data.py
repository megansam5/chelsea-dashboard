import os
import json
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from moto import mock_aws

import extract_data


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    """Automatically set AWS credentials for boto3 mock."""
    monkeypatch.setenv("AWS_ACCESS_KEY", "fake_access_key")
    monkeypatch.setenv("AWS_SECRET_KEY", "fake_secret_key")


@pytest.fixture
def mock_wrapped_request():
    """Mock response from wrappedRequest."""
    mock_response = MagicMock()
    mock_result = {
        "result": MagicMock(
            status_code=200,
            url="http://fakeapi.com/test",
            text=json.dumps({"foo": "bar"})
        )
    }
    mock_response.get = MagicMock(return_value=mock_result["result"])
    return mock_response

def test_ingest_data_writes_file(tmp_path, mock_wrapped_request):
    """Test that ingest_data writes API response JSON to file."""
    fake_url = "http://fakeapi.com/"
    fake_key = "abc123"
    fake_api_name = "endpoint"
    fake_file_name = "data.json"
    file_path = tmp_path

    with patch("extract_data.wrappedRequest", return_value=mock_wrapped_request):
        extract_data.ingest_data(fake_url, fake_key, file_path, fake_api_name, fake_file_name)

    output_file = file_path / fake_file_name
    assert output_file.exists(), "Output JSON file should be created"

    with open(output_file, encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"foo": "bar"}, "File content should match API response"


def test_ingest_data_raises_on_error(tmp_path):
    """Test that ingest_data raises exception on request failure."""
    with patch("extract_data.wrappedRequest", side_effect=Exception("API Error")):
        with pytest.raises(Exception, match="API Error"):
            extract_data.ingest_data("url", "key", tmp_path, "api", "file.json")


@mock_aws
def test_upload_json_to_s3_uploads(monkeypatch):
    """Test upload_json_to_s3 uploads to S3 using moto mock."""
    import boto3

    s3 = boto3.client("s3")
    bucket_name = "test-bucket"
    s3.create_bucket(Bucket=bucket_name)

    json_data = {"hello": "world"}

    extract_data.upload_json_to_s3(json_data, bucket_name, "data.json")

    response = s3.get_object(Bucket=bucket_name, Key="data.json")
    content = json.loads(response["Body"].read().decode("utf-8"))
    assert content == json_data


@mock_aws
def test_upload_json_to_s3_raises_on_error(monkeypatch):
    """Test upload_json_to_s3 raises on boto3 failure."""
    json_data = {"test": "data"}

    with patch("boto3.client") as mock_client:
        mock_client.return_value.put_object.side_effect = Exception("S3 Error")
        with pytest.raises(Exception, match="S3 Error"):
            extract_data.upload_json_to_s3(json_data, "fake-bucket", "data.json")


@mock_aws
def test_ingest_data_to_s3_combined_flow(mock_wrapped_request):
    """Test full flow: API ingestion + S3 upload."""
    import boto3

    s3 = boto3.client("s3")
    bucket_name = "combined-bucket"
    s3.create_bucket(Bucket=bucket_name)

    with patch("extract_data.wrappedRequest", return_value=mock_wrapped_request):
        extract_data.ingest_data_to_s3(
            url="http://fakeapi.com/",
            key="xyz",
            bucket_name=bucket_name,
            api_name="endpoint",
            s3_filename="output.json",
        )

    response = s3.get_object(Bucket=bucket_name, Key="output.json")
    content = json.loads(response["Body"].read().decode("utf-8"))
    assert content == {"foo": "bar"}, "S3 object should contain API JSON data"
