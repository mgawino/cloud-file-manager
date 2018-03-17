# -*- coding: utf-8 -*-
import boto3
import os

from cloud_file_manager.services.s3_client import S3Client


class DataManager:

    def __init__(self, s3_client: S3Client):
        self.s3_client = s3_client

    @staticmethod
    def create_from_environ():
        boto_s3_client = boto3.client('s3', endpoint_url=os.environ.get('S3_ENDPOINT_URL'))
        s3_client = S3Client(boto_s3_client)
        return DataManager(s3_client)

    @staticmethod
    def _create_node(text, s3_key):
        if s3_key == '':
            type = 'bucket'
        elif '.' in s3_key:
            type = 'file'
        else:
            type = 'folder'
        return {
            'text': text,
            'type': type,
            'children': []
        }

    def _add_node(self, tree, s3_key):
        if s3_key not in tree:
            node = self._create_node(
                text=os.path.basename(s3_key),
                s3_key=s3_key
            )
            tree[s3_key] = node
            splitted = s3_key.rsplit('/')
            parent_s3_key = '' if len(splitted) == 1 else splitted[0]
            parent_node = self._add_node(tree, parent_s3_key)
            parent_node['children'].append(node)
            return node
        else:
            return tree[s3_key]

    def _create_tree(self, bucket_name):
        bucket_keys = self.s3_client.list_bucket_keys(bucket_name)
        tree = {'': self._create_node(text=bucket_name, s3_key='')}
        for s3_key in bucket_keys:
            self._add_node(tree, s3_key)
        return tree['']

    def get_tree(self):
        bucket_names = self.s3_client.list_bucket_names()
        bucket_nodes = map(self._create_tree, bucket_names)
        return list(bucket_nodes)

    def create_node(self, node):
        pass

    def rename_node(self, node):
        pass

    def delete_node(self, node):
        pass
