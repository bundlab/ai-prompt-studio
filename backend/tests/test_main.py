import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to AI Prompt Studio API",
        "docs": "/docs",
        "version": "0.1.0",
    }


def test_openapi_documents_existing_api_schemas(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200

    openapi = response.json()
    assert "UserCreate" in openapi["components"]["schemas"]
    assert "ErrorResponse" in openapi["components"]["schemas"]

    register = openapi["paths"]["/auth/register"]["post"]
    assert register["summary"] == "Register a user"
    assert "400" in register["responses"]
    assert "500" in register["responses"]

    login = openapi["paths"]["/auth/login"]["post"]
    assert login["summary"] == "Authenticate a user"
    assert "401" in login["responses"]
    assert "500" in login["responses"]
    login_example = login["requestBody"]["content"]["application/x-www-form-urlencoded"]["examples"]
    assert "valid_credentials" in login_example

    current_user = openapi["paths"]["/users/me"]["get"]
    assert current_user["summary"] == "Get the current user"
    assert "404" in current_user["responses"]
    assert "500" in current_user["responses"]