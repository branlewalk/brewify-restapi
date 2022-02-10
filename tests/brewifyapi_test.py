import pytest

from brewifyapi import create_app, db

@pytest.fixture
def client():
    app = create_app('TestConfig')

    with app.test_client() as client:
        with app.app_context():
            db.open_connection()
        yield client
        
def test_empty_db(client):
    rv = client.get('/')
    assert b'No entries here so far' in rv.data