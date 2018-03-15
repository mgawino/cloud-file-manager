from flask import Flask, render_template, jsonify, send_from_directory, Response

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tree', methods=['GET'])
def tree():
    return jsonify([
        {
            'id': 'node_2',
            'text': 'Bucket 1',
            'type': 'bucket',
            'children': [
                {
                    'text': 'Folder 1',
                    'type': 'folder',
                    'children': [{'text': 'file1', 'type': 'file'}]
                },
                {
                    'text': 'Folder 2',
                    'type': 'folder'
                }
            ]
        }
    ])


@app.route('/node', methods=['POST'])
def node_create():
    return Response()


@app.route('/node', methods=['PUT'])
def node_rename():
    return Response()


@app.route('/node', methods=['DELETE'])
def node_delete():
    return Response()


if __name__ == '__main__':
    app.run(debug=True)
