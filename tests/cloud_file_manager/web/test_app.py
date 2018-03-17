import json

import pytest
import flask_injector
from flask_injector import FlaskInjector

from cloud_file_manager.services.data_manager import DataManager
from cloud_file_manager.web.app import app


@pytest.fixture()
def flask_app(data_manager):

    def configure(binder):
        binder.bind(
            DataManager,
            to=data_manager,
            scope=flask_injector.request
        )

    FlaskInjector(app=app, modules=[configure])

    return app


@pytest.fixture()
def app_test_client(flask_app):
    return flask_app.test_client()


def test_app_index(app_test_client):
    response = app_test_client.get('/')

    assert response.status_code == 200


def test_app_tree(app_test_client, boto_s3_client):
    boto_s3_client.create_bucket_with_empty_keys(
        bucket_name='bucket',
        keys=['a/b', 'a/c']
    )

    response = app_test_client.get('/tree')
    tree = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert tree == [
        {
            'text': 'bucket',
            'type': 'bucket',
            'children': [
                {
                    'text': 'a',
                    'type': 'folder',
                    'children': [
                        {'text': 'b', 'type': 'folder', 'children': []},
                        {'text': 'c', 'type': 'folder', 'children': []}
                    ]
                }
            ]
        }
    ]


def test_app_create_node(app_test_client):
    response = app_test_client.post('/node')

    assert response.status_code == 200


def test_app_rename_node(app_test_client):
    response = app_test_client.put('/node')

    assert response.status_code == 200


def test_app_delete_node(app_test_client):
    response = app_test_client.delete('/node')

    assert response.status_code == 200
