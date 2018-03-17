# -*- coding: utf-8 -*-


def test_list_bucket_names(s3_client, boto_s3_client):
    boto_s3_client.create_bucket(Bucket='bucket1')
    boto_s3_client.create_bucket(Bucket='bucket2')

    bucket_names = s3_client.list_bucket_names()

    assert bucket_names == ['bucket1', 'bucket2']


def test_list_bucket_keys(s3_client, boto_s3_client):
    boto_s3_client.create_bucket_with_empty_keys(
        'bucket',
        ['a/b/c', 'a/d/e']
    )

    bucket_keys = s3_client.list_bucket_keys('bucket')
    sorted_keys = sorted(bucket_keys)

    assert sorted_keys == ['a/b/c', 'a/d/e']
