# -*- coding: utf-8 -*-
import operator

import functools


class S3Client:

    def __init__(self, boto_s3_client):
        self.boto_s3_client = boto_s3_client

    def list_bucket_names(self):
        response = self.boto_s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        return list(map(operator.itemgetter('Name'), buckets))

    def list_bucket_keys(self, bucket_name, s3_prefix=None):
        list_objects = functools.partial(
            self.boto_s3_client.list_objects, Bucket=bucket_name
        )
        response = list_objects() if s3_prefix is None else list_objects(Prefix=s3_prefix)
        keys = response.get('Contents', [])
        return list(map(operator.itemgetter('Key'), keys))

    def create_bucket(self, bucket_name):
        self.boto_s3_client.create_bucket(Bucket=bucket_name)

    def delete_bucket(self, bucket_name):
        self.boto_s3_client.delete_bucket(Bucket=bucket_name)

    def create_keys(self, bucket_name, s3_keys):
        for s3_key in s3_keys:
            self.boto_s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=b'')

    def delete_keys(self, bucket_name, s3_prefix=None):
        keys_to_delete = self.list_bucket_keys(bucket_name, s3_prefix)
        objects_to_delete = [{'Key': key} for key in keys_to_delete]
        if objects_to_delete:
            self.boto_s3_client.delete_objects(
                Bucket=bucket_name,
                Delete={'Objects': objects_to_delete}
            )

    def move_keys(self, bucket_name, source_s3_prefix, destination_s3_prefix):
        source_keys = self.list_bucket_keys(bucket_name, source_s3_prefix)
        new_keys = [key.replace(source_s3_prefix, destination_s3_prefix)
                    for key in source_keys]
        self.create_keys(bucket_name, new_keys)
        self.delete_keys(bucket_name, source_s3_prefix)

    def copy_bucket(self, source_bucket, destination_bucket):
        source_keys = self.list_bucket_keys(source_bucket)
        self.create_keys(destination_bucket, source_keys)
