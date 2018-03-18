# -*- coding: utf-8 -*-
import os


class JSTreeBuilder:

    @staticmethod
    def _create_node(text, s3_key):
        if s3_key == '':
            type = 'bucket'
        else:
            type = 'folder'
        return {
            'text': text,
            'type': type,
            'children': []
        }

    def _add_node(self, tree, s3_key):
        if s3_key not in tree:
            node = self._create_node(text=os.path.basename(s3_key), s3_key=s3_key)
            tree[s3_key] = node
            splitted = s3_key.rsplit('/')
            parent_s3_key = '' if len(splitted) == 1 else splitted[0]
            parent_node = self._add_node(tree, parent_s3_key)
            parent_node['children'].append(node)
            return node
        else:
            return tree[s3_key]

    def make_json_tree(self, bucket_name, bucket_keys):
        tree = {'': self._create_node(text=bucket_name, s3_key='')}
        for s3_key in bucket_keys:
            self._add_node(tree, s3_key)
        return tree['']
