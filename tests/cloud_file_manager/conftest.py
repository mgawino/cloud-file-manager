# -*- coding: utf-8 -*-

import boto3
import pytest

from cloud_file_manager.services.data_manager import DataManager
from cloud_file_manager.services.s3_client import S3Client


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

    def create_bucket_with_empty_keys(bucket_name, keys):
        client.create_bucket(Bucket=bucket_name)
        for key in keys:
            client.put_object(Bucket=bucket_name, Key=key, Body=b'')

    client = boto3.client(
        's3',
        endpoint_url='http://localhost:4572',
        aws_access_key_id='test_access_key',
        aws_secret_access_key='test_secret_key'
    )
    client.create_bucket_with_empty_keys = create_bucket_with_empty_keys
    request.addfinalizer(delete_all_buckets)

    return client


@pytest.fixture()
def s3_client(boto_s3_client):
    return S3Client(boto_s3_client)


@pytest.fixture()
def data_manager(s3_client):
    return DataManager(s3_client)
