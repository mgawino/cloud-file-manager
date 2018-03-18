# -*- coding: utf-8 -*-
import os


class JSTreeBuilder:

    @staticmethod
    def _create_node(node_name, path):
        if path == '':
            type = 'bucket'
        else:
            type = 'folder'
        return {
            'text': node_name,
            'type': type,
            'children': []
        }

    def _add_node(self, tree, path):
        if path not in tree:
            node = self._create_node(node_name=os.path.basename(path), path=path)
            tree[path] = node
            splitted = path.rsplit('/')
            parent_s3_key = '' if len(splitted) == 1 else splitted[0]
            parent_node = self._add_node(tree, parent_s3_key)
            parent_node['children'].append(node)
            return node
        else:
            return tree[path]

    def make_json_tree(self, root_name, paths):
        tree = {'': self._create_node(node_name=root_name, path='')}
        for s3_key in paths:
            self._add_node(tree, s3_key)
        return tree['']
