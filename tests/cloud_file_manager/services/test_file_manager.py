# -*- coding: utf-8 -*-
import operator

from cloud_file_manager.services.file_manager import FileManager


def test_create_from_config():
    file_manager = FileManager.create_from_environ()


def test_get_tree_with_many_roots(file_manager):
    file_manager.create_node('test')
    file_manager.create_node('test2')
    file_manager.create_node('test/a')
    file_manager.create_node('test2/a')

    tree = file_manager.get_tree()
    sorted_tree = sorted(tree, key=operator.itemgetter('text'))

    assert sorted_tree == [
        {
            'text': 'test',
            'type': 'bucket',
            'children': [
                {
                    'text': 'a',
                    'type': 'folder',
                    'children': []
                }
            ]
        },
        {
            'text': 'test2',
            'type': 'bucket',
            'children': [
                {
                    'text': 'a',
                    'type': 'folder',
                    'children': []
                }
            ]
        }
    ]


def test_rename_node(file_manager):
    file_manager.create_node('test')
    file_manager.create_node('test/a')
    file_manager.create_node('test/a/b')

    file_manager.rename_node('test/a', 'test/c')
    tree = file_manager.get_tree()

    assert tree == [
        {
            'text': 'test',
            'type': 'bucket',
            'children': [
                {
                    'text': 'c',
                    'type': 'folder',
                    'children': [{'text': 'b', 'type': 'folder', 'children': []}]
                }
            ]
        }
    ]


def test_delete_root_node(file_manager):
    file_manager.create_node('test')
    file_manager.create_node('test/a')

    file_manager.delete_node('test')
    tree = file_manager.get_tree()

    assert tree == []