# -*- coding: utf-8 -*-
import operator


class S3Client:

    def __init__(self, boto_s3_client):
        self.boto_s3_client = boto_s3_client

    def list_bucket_names(self):
        response = self.boto_s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        return list(map(operator.itemgetter('Name'), buckets))

    def list_bucket_keys(self, bucket_name):
        response = self.boto_s3_client.list_objects(Bucket=bucket_name)
        keys = response.get('Contents', [])
        return list(map(operator.itemgetter('Key'), keys))
