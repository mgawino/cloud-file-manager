# -*- coding: utf-8 -*-
import operator
from unittest.mock import Mock, call

from cloud_file_manager.services.file_manager import FileManager

# Integration tests


def test_create_from_config():
    file_manager = FileManager.create_from_environ()


def test_get_tree_with_many_roots(file_manager):
    file_manager.create_node('test1')
    file_manager.create_node('test2')
    file_manager.create_node('test1/a')
    file_manager.create_node('test2/a')

    tree = file_manager.get_tree()
    sorted_tree = sorted(tree, key=operator.itemgetter('text'))

    assert sorted_tree == [
        {
            'text': 'test1',
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


# Tests with mocks


def test_get_tree(file_manager_mock, s3_client_mock):
    bucket_to_keys = {
        'test1': ['a', 'a/b'],
        'test2': ['c', 'c/d']
    }
    s3_client_mock.list_bucket_names.return_value = ['test1', 'test2']
    s3_client_mock.list_bucket_keys.side_effect = bucket_to_keys.get

    tree = file_manager_mock.get_tree()
    sorted_tree = sorted(tree, key=operator.itemgetter('text'))

    assert sorted_tree == [
        {
            'text': 'test1',
            'type': 'bucket',
            'children': [
                {
                    'text': 'a',
                    'type': 'folder',
                    'children': [{'text': 'b', 'type': 'folder', 'children': []}]
                }
            ]
        },
        {
            'text': 'test2',
            'type': 'bucket',
            'children': [
                {
                    'text': 'c',
                    'type': 'folder',
                    'children': [{'text': 'd', 'type': 'folder', 'children': []}]
                }
            ]
        }
    ]


def test_create_node_with_root_path(file_manager_mock, s3_client_mock):
    file_manager_mock.create_node('root')

    s3_client_mock.create_bucket.assert_called_once_with('root')


def test_create_node_with_nested_path(file_manager_mock, s3_client_mock):
    file_manager_mock.create_node('root/a/b')

    s3_client_mock.create_keys.assert_called_once_with('root', ['a/b'])


def test_rename_node_with_new_root(file_manager_mock, s3_client_mock):
    manager = Mock()
    manager.attach_mock(s3_client_mock.create_bucket, 'create_bucket')
    manager.attach_mock(s3_client_mock.copy_bucket, 'copy_bucket')
    manager.attach_mock(s3_client_mock.delete_keys, 'delete_keys')
    manager.attach_mock(s3_client_mock.delete_bucket, 'delete_bucket')

    file_manager_mock.rename_node('root1/a/b', 'root2/a/b')

    expected_calls = [
        call.create_bucket('root2'),
        call.copy_bucket(source_bucket='root1', destination_bucket='root2'),
        call.delete_keys('root1'),
        call.delete_bucket('root1')
    ]
    assert manager.method_calls == expected_calls
