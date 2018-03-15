import boto3
import pytest

from cloud_file_manager.services.data_manager import DataManager
from cloud_file_manager.web.app import app


@pytest.fixture()
def s3_client():
    return boto3.client(
        's3',
        endpoint_url='http://localhost:4572',
        aws_access_key_id='test_access_key',
        aws_secret_access_key='test_secret_key'
    )


@pytest.fixture()
def data_manager(s3_client):
    return DataManager(s3_client)


@pytest.fixture()
def app_test_client():
    return app.test_client()


def test_app_index(app_test_client):
    response = app_test_client.get('/')

    assert response.status_code == 200


def test_app_tree(app_test_client):
    response = app_test_client.get('/tree')

    assert response.status_code == 200


def test_app_create_node(app_test_client):
    response = app_test_client.post('/node')

    assert response.status_code == 200


def test_app_rename_node(app_test_client):
    response = app_test_client.put('/node')

    assert response.status_code == 200


def test_app_delete_node(app_test_client):
    response = app_test_client.delete('/node')

    assert response.status_code == 200
