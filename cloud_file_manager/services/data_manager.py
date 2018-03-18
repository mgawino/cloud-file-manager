# -*- coding: utf-8 -*-
import boto3
import os

from cloud_file_manager.services.s3_client import S3Client
from cloud_file_manager.services.tree_builder import JSTreeBuilder


class DataManager:

    def __init__(self, s3_client: S3Client, tree_builder: JSTreeBuilder):
        self.s3_client = s3_client
        self.tree_builder = tree_builder

    @staticmethod
    def create_from_environ():
        boto_s3_client = boto3.client('s3', endpoint_url=os.environ.get('S3_ENDPOINT_URL'))
        s3_client = S3Client(boto_s3_client)
        js_tree_builder = JSTreeBuilder()
        return DataManager(s3_client, js_tree_builder)

    @staticmethod
    def _split_path(path):
        splitted = path.split(os.sep, 1)
        if len(splitted) == 1:
            return splitted[0], ''
        else:
            return splitted

    def get_tree(self):
        bucket_names = self.s3_client.list_bucket_names()
        trees = []
        for bucket_name in bucket_names:
            bucket_keys = self.s3_client.list_bucket_keys(bucket_name)
            trees.append(self.tree_builder.make_json_tree(bucket_name, bucket_keys))
        return list(trees)

    def create_node(self, path):
        bucket_name, s3_key = self._split_path(path)
        if not s3_key:
            self.s3_client.create_bucket(bucket_name)
        else:
            self.s3_client.create_key(bucket_name, s3_key)

    def rename_node(self, old_path, new_path):
        old_bucket_name, old_s3_key = self._split_path(old_path)
        new_bucket_name, new_s3_key = self._split_path(new_path)
        if old_bucket_name != new_bucket_name:
            self.s3_client.create_bucket(new_bucket_name)
            self.s3_client.copy_bucket(
                source_bucket=old_bucket_name,
                destination_bucket=new_bucket_name
            )
            self.s3_client.delete_bucket(old_bucket_name)
        else:
            self.s3_client.move_keys(
                bucket_name=new_bucket_name,
                source_s3_prefix=old_s3_key,
                destination_s3_prefix=new_s3_key
            )

    def delete_node(self, path):
        bucket_name, s3_key = self._split_path(path)
        s3_prefix = s3_key if s3_key else None
        self.s3_client.delete_keys(bucket_name, s3_prefix)
        if s3_prefix is None:
            self.s3_client.delete_bucket(bucket_name)
