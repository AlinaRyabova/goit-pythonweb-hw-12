import pytest
from fastapi.testclient import TestClient
from main import app  
from unittest.mock import MagicMock
from unittest.mock import patch

client = TestClient(app)



def test_healthchecker_success():
    response = client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "APP is healthy"}

@patch("src.api.utils.get_db")
def test_healthchecker_database_error(mock_db):
    mock_db.execute.side_effect = Exception("Database connection error")
    response = client.get("/api/healthchecker")
    assert response.status_code == 500
    assert response.json() == {"detail": "Error connecting to the database"}

@patch("src.api.utils.get_db")
def test_healthchecker_database_not_configured(mock_db):
    mock_db.execute.return_value.scalar_one_or_none.return_value = None
    response = client.get("/api/healthchecker")
    assert response.status_code == 500
    assert response.json() == {"detail": "Database is not configured correctly"}