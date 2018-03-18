# -*- coding: utf-8 -*-
from cloud_file_manager.services.file_manager import FileManager


def test_file_manager_create_from_config():
    file_manager = FileManager.create_from_environ()


def test_get_tree(file_manager):
    file_manager.create_node('test')
    file_manager.create_node('test/a')
    file_manager.create_node('test/a/b')

    tree = file_manager.get_tree()

    assert tree == [
        {
            'text': 'test',
            'type': 'bucket',
            'children': [
                {
                    'text': 'a',
                    'type': 'folder',
                    'children': [
                        {
                            'text': 'b',
                            'type': 'folder',
                            'children': []
                        }
                    ]
                }
            ]
        }
    ]


def test_rename_node(file_manager):
    file_manager.create_node('test')
    file_manager.create_node('test/a')

    file_manager.rename_node('test', 'test2')
    tree = file_manager.get_tree()

    assert tree == [
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


def test_delete_node(file_manager):
    file_manager.create_node('test')
    file_manager.create_node('test/a')

    file_manager.delete_node('test')
    tree = file_manager.get_tree()

    assert tree == []