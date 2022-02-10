import pytest
import brewifyapi

@pytest.fixture
def client():
    brewifyapi.app.config["TESTING"] = True
    with brewifyapi.app.test_client() as client:
        yield client
