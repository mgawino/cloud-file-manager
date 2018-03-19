# -*- coding: utf-8 -*-
import itertools


class JSTreeBuilder:

    _ROOT_TYPE = 'bucket'
    _CHILD_TYPE = 'folder'

    def __init__(self, delimiter='/'):
        self.delimiter = delimiter

    @staticmethod
    def _create_node(node_name, type):
        return {
            'text': node_name,
            'type': type,
            'children': []
        }

    def _iter_nodes_info(self, root_name, paths):
        for path in paths:
            path_with_root = self.delimiter.join((root_name, path))
            parent_path, node_name = path_with_root.rsplit(self.delimiter, 1)
            node_info = {
                'parent_path': parent_path,
                'node_name': node_name,
                'node_path': path_with_root
            }
            yield node_info

    def _build_tree(self, root_name, nodes_info):
        group_by_parent = lambda node_info: node_info['parent_path']
        tree = {root_name: self._create_node(root_name, self._ROOT_TYPE)}
        for parent_path, children in itertools.groupby(nodes_info, key=group_by_parent):
            assert parent_path in tree
            parent = tree[parent_path]
            children_nodes = []
            for child in children:
                child_node = self._create_node(child['node_name'], self._CHILD_TYPE)
                children_nodes.append(child_node)
                tree[child['node_path']] = child_node
            parent['children'] = children_nodes
        return tree

    def make_json_tree(self, root_name, paths):
        sorted_paths = sorted(paths)
        nodes_info = self._iter_nodes_info(root_name, sorted_paths)
        tree = self._build_tree(root_name, nodes_info)
        return tree[root_name]
