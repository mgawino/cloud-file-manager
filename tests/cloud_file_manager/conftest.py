# -*- coding: utf-8 -*-
import json
from unittest.mock import Mock

import boto3
import flask_injector
from flask_injector import FlaskInjector
import pytest
from cached_property import cached_property
from cloud_file_manager.web.app import app
from flask.testing import FlaskClient
from werkzeug.wrappers import BaseResponse

from cloud_file_manager.services.file_manager import FileManager
from cloud_file_manager.services.s3_client import S3Client
from cloud_file_manager.services.tree_builder import JSTreeBuilder


@pytest.fixture()
def boto_s3_client(request):

    def delete_bucket_objects(bucket_name):
        objects = client.list_objects(Bucket=bucket_name).get('Contents', [])
        object_dicts = [{'Key': obj['Key']} for obj in objects]
        client.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': object_dicts}
        )

    def delete_all_buckets():
        buckets = client.list_buckets().get('Buckets', [])
        for bucket in buckets:
            delete_bucket_objects(bucket['Name'])
            client.delete_bucket(Bucket=bucket['Name'])

    client = boto3.client(
        's3',
        endpoint_url='http://localhost:4572',
        aws_access_key_id='test_access_key',
        aws_secret_access_key='test_secret_key'
    )
    request.addfinalizer(delete_all_buckets)

    return client


@pytest.fixture()
def s3_client(boto_s3_client):
    return S3Client(boto_s3_client)


@pytest.fixture()
def js_tree_builder():
    return JSTreeBuilder()


@pytest.fixture()
def file_manager(s3_client, js_tree_builder):
    return FileManager(s3_client, js_tree_builder)


@pytest.fixture()
def flask_app():

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

    app.response_class = Response
    app.test_client_class = TestClient
    app.testing = True

    return app


@pytest.fixture()
def app_test_client(flask_app, file_manager):

    def configure(binder):
        binder.bind(
            FileManager,
            to=file_manager,
            scope=flask_injector.request
        )

    FlaskInjector(app=flask_app, modules=[configure])

    return flask_app.test_client()


@pytest.fixture()
def file_manager_mock():
    return Mock(spec_set=FileManager)


@pytest.fixture()
def mocked_app_test_client(flask_app, file_manager_mock):

    def configure(binder):
        binder.bind(
            FileManager,
            to=file_manager_mock,
            scope=flask_injector.request
        )

    FlaskInjector(app=app, modules=[configure])

    return flask_app.test_client()