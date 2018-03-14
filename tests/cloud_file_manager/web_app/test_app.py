import pytest

from cloud_file_manager.web.app import app


@pytest.fixture()
def app_test_client():
    return app.test_client()


def test_app(app_test_client):
    response = app_test_client.get('/')

    assert response.status_code == 200
