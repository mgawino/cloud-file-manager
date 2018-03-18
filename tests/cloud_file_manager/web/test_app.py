import json

import pytest
import flask_injector
from cached_property import cached_property
from flask.testing import FlaskClient
from flask_injector import FlaskInjector
from werkzeug.wrappers import BaseResponse

from cloud_file_manager.services.file_manager import FileManager
from cloud_file_manager.web.app import app


@pytest.fixture()
def flask_app(file_manager):

    def configure(binder):
        binder.bind(
            FileManager,
            to=file_manager,
            scope=flask_injector.request
        )

    FlaskInjector(app=app, modules=[configure])

    return app


@pytest.fixture()
def app_test_client(flask_app):

    class Response(BaseResponse):
        @cached_property
        def json(self):
            return json.loads(self.data.decode('utf-8'))

    class TestClient(FlaskClient):
        def open(self, *args, **kwargs):
            if 'json' in kwargs:
                kwargs['data'] = json.dumps(kwargs.pop('json'))
                kwargs['content_type'] = 'application/json'
            return super(TestClient, self).open(*args, **kwargs)

    flask_app.response_class = Response
    flask_app.test_client_class = TestClient
    flask_app.testing = True

    return flask_app.test_client()


def test_app_index(app_test_client):
    response = app_test_client.get('/')

    assert response.status_code == 200


def test_app_create_node(app_test_client):
    create_response1 = app_test_client.post('/node', json={'path': 'test'})
    create_response2 = app_test_client.post('/node', json={'path': 'test/a'})

    tree_response = app_test_client.get('/tree')

    assert create_response1.status_code == 200
    assert create_response2.status_code == 200
    assert tree_response.status_code == 200
    assert tree_response.json == [
        {
            'text': 'test',
            'type': 'bucket',
            'children': [{'text': 'a', 'type': 'folder', 'children': []}]
        }
    ]


def test_app_rename_node(app_test_client):
    create_response1 = app_test_client.post('/node', json={'path': 'test'})
    create_response2 = app_test_client.post('/node', json={'path': 'test/a'})
    create_response3 = app_test_client.post('/node', json={'path': 'test/a/b'})

    rename_response = app_test_client.put(
        '/node',
        json={'old_path': 'test/a', 'new_path': 'test/c'}
    )
    tree_response = app_test_client.get('/tree')

    assert create_response1.status_code == 200
    assert create_response2.status_code == 200
    assert create_response3.status_code == 200
    assert rename_response.status_code == 200
    assert tree_response.status_code == 200
    assert tree_response.json == [
        {
            'text': 'test',
            'type': 'bucket',
            'children': [
                {
                    'text': 'c',
                    'type': 'folder',
                    'children': [{'text': 'b', 'type': 'folder', 'children': []}]
                }
            ]
        }
    ]


def test_app_delete_node(app_test_client):
    create_response1 = app_test_client.post('/node', json={'path': 'test'})
    create_response2 = app_test_client.post('/node', json={'path': 'test/a'})

    delete_response = app_test_client.delete('/node', json={'path': 'test/a'})
    tree_response = app_test_client.get('/tree', json={'path': 'test/a'})

    assert create_response1.status_code == 200
    assert create_response2.status_code == 200
    assert delete_response.status_code == 200
    assert tree_response.status_code == 200
    assert tree_response.json == [
        {
            'text': 'test',
            'type': 'bucket',
            'children': []
        }
    ]
