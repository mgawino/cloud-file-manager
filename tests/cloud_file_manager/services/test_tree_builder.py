# -*- coding: utf-8 -*-


def test_with_nested_tree(js_tree_builder):
    tree = js_tree_builder.make_json_tree(
        root_name='root',
        paths=['a', 'a/b', 'a/b/c']
    )

    assert tree == {
        'text': 'root',
        'type': 'bucket',
        'children': [
            {
                'text': 'a',
                'type': 'folder',
                'children': [
                    {
                        'text': 'b',
                        'type': 'folder',
                        'children': [
                            {
                                'text': 'c',
                                'type': 'folder',
                                'children': []
                            }
                        ]
                    }
                ]
            }
        ]
    }


def test_with_many_children(js_tree_builder):
    tree = js_tree_builder.make_json_tree(
        root_name='root',
        paths=['a', 'a/b', 'a/c']
    )

    assert tree == {
        'text': 'root',
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
                    },
                    {
                        'text': 'c',
                        'type': 'folder',
                        'children': []
                    }
                ]
            }
        ]
    }