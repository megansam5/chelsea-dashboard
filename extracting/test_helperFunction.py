import os
import csv
import pytest
from unittest.mock import patch, MagicMock
from helperFunction import removeCSV, writeData2CSV, wrappedRequest


def test_remove_csv_deletes_matching_files(tmp_path):
    """Test that removeCSV deletes all CSV files with a matching prefix."""
    prefix = "datafile"
    filenames = [
        f"{prefix}_1.csv",
        f"{prefix}_2.CSV", 
        "otherfile.csv"
    ]

    for f in filenames:
        (tmp_path / f).write_text("test")

    removeCSV(prefix, tmp_path)

    remaining_files = [f.name for f in tmp_path.iterdir()]
    assert "otherfile.csv" in remaining_files
    assert not any(f.startswith(prefix) for f in remaining_files), "Prefixed CSV files should be deleted"


def test_remove_csv_raises_on_error(monkeypatch):
    """Test that removeCSV raises if os.listdir fails."""
    monkeypatch.setattr("os.listdir", lambda _: (_ for _ in ()).throw(OSError("Permission denied")))
    with pytest.raises(Exception, match="Permission denied"):
        removeCSV("prefix", "fakepath")


def test_write_data_to_csv_creates_file_with_correct_content(tmp_path):
    """Test writeData2CSV writes correct CSV data."""
    file_name = "output.csv"
    cols = ["name", "age"]
    rows = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

    writeData2CSV(file_name, tmp_path, cols, rows)

    file_path = tmp_path / file_name
    assert file_path.exists(), "CSV file should be created"

    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    assert data == [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]


def test_write_data_to_csv_raises_on_error(monkeypatch, tmp_path):
    """Test writeData2CSV raises if file cannot be written."""
    monkeypatch.setattr("builtins.open", lambda *a, **k: (_ for _ in ()).throw(IOError("Disk full")))
    with pytest.raises(Exception, match="Disk full"):
        writeData2CSV("file.csv", tmp_path, ["col"], [{"col": "val"}])



def test_wrapped_request_success(monkeypatch):
    """Test wrappedRequest returns result when request succeeds."""
    mock_response = MagicMock(status_code=200)
    monkeypatch.setattr("helperFunction.get", lambda *a, **k: mock_response)

    result = wrappedRequest("http://fakeapi.com", {}, {"X-Auth-Token": "abc"})
    assert result["result"].status_code == 200
    assert result["retry"] == 0


@patch("helperFunction.get")
@patch("helperFunction.sleep")
def test_wrapped_request_retries_on_failure(mock_sleep, mock_get):
    """Test wrappedRequest retries when non-200 responses occur."""
    mock_get.side_effect = [
        MagicMock(status_code=500),
        MagicMock(status_code=500),
        MagicMock(status_code=200)
    ]

    result = wrappedRequest("http://fakeapi.com", {}, {}, retry=3)
    assert result["result"].status_code == 200
    assert mock_get.call_count == 3
    assert mock_sleep.called


@patch("helperFunction.get", side_effect=Exception("Network error"))
@patch("helperFunction.sleep")
def test_wrapped_request_raises_after_all_retries(mock_sleep, mock_get):
    """Test wrappedRequest raises after max retries."""
    with pytest.raises(Exception):
        wrappedRequest("http://fakeapi.com", {}, {}, retry=2)
    assert mock_get.call_count == 2
    assert mock_sleep.called
