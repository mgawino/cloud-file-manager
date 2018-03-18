# -*- coding: utf-8 -*-


def test_list_bucket_names(s3_client):
    s3_client.create_bucket('bucket1')
    s3_client.create_bucket('bucket2')

    bucket_names = s3_client.list_bucket_names()

    assert bucket_names == ['bucket1', 'bucket2']


def test_list_bucket_keys(s3_client):
    s3_client.create_bucket('bucket')
    s3_client.create_keys('bucket', ['a/b/c', 'a/d/e'])

    bucket_keys = s3_client.list_bucket_keys('bucket')
    sorted_keys = sorted(bucket_keys)

    assert sorted_keys == ['a/b/c', 'a/d/e']


def test_move_keys(s3_client):
    s3_client.create_bucket('bucket')
    s3_client.create_keys('bucket', ['a/b/c', 'a/b/d'])

    s3_client.move_keys('bucket', 'a/b', 'a/e')
    sorted_keys = sorted(s3_client.list_bucket_keys('bucket'))

    assert sorted_keys == ['a/e/c', 'a/e/d']


def test_copy_bucket(s3_client):
    s3_client.create_bucket('bucket1')
    s3_client.create_bucket('bucket2')
    s3_client.create_keys('bucket1', ['a/b', 'c/d'])

    s3_client.copy_bucket('bucket1', 'bucket2')
    first_bucket_keys = s3_client.list_bucket_keys('bucket1')
    second_bucket_keys = s3_client.list_bucket_keys('bucket2')

    assert sorted(first_bucket_keys) == ['a/b', 'c/d']
    assert sorted(second_bucket_keys) == ['a/b', 'c/d']
