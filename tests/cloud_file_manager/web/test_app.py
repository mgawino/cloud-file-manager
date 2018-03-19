

def test_index(app_test_client):
    response = app_test_client.get('/')

    assert response.status_code == 200


def test_create_node(app_test_client):
    create_response1 = app_test_client.post('/node', json={'path': 'test'})
    create_response2 = app_test_client.post('/node', json={'path': 'test/a'})

    tree_response = app_test_client.get('/tree')

    assert create_response1.status_code == 200
    assert create_response2.status_code == 200
    assert tree_response.status_code == 200
    assert tree_response.json == [
        {
            'text': 'test',
            'type': 'bucket',
            'children': [{'text': 'a', 'type': 'folder', 'children': []}]
        }
    ]


def test_rename_node(app_test_client):
    create_response1 = app_test_client.post('/node', json={'path': 'test'})
    create_response2 = app_test_client.post('/node', json={'path': 'test/a'})
    create_response3 = app_test_client.post('/node', json={'path': 'test/a/b'})

    rename_response = app_test_client.put(
        '/node',
        json={'old_path': 'test/a', 'new_path': 'test/c'}
    )
    tree_response = app_test_client.get('/tree')

    assert create_response1.status_code == 200
    assert create_response2.status_code == 200
    assert create_response3.status_code == 200
    assert rename_response.status_code == 200
    assert tree_response.status_code == 200
    assert tree_response.json == [
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


def test_delete_node(app_test_client):
    create_response1 = app_test_client.post('/node', json={'path': 'test'})
    create_response2 = app_test_client.post('/node', json={'path': 'test/a'})

    delete_response = app_test_client.delete('/node', json={'path': 'test/a'})
    tree_response = app_test_client.get('/tree', json={'path': 'test/a'})

    assert create_response1.status_code == 200
    assert create_response2.status_code == 200
    assert delete_response.status_code == 200
    assert tree_response.status_code == 200
    assert tree_response.json == [
        {
            'text': 'test',
            'type': 'bucket',
            'children': []
        }
    ]
