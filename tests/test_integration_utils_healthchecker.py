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


