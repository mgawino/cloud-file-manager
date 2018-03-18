import flask_injector
from flask_injector import FlaskInjector
from flask import Flask, render_template, jsonify, send_from_directory, Response, request

from cloud_file_manager.services.data_manager import DataManager

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tree', methods=['GET'])
def tree(data_manager: DataManager):
    tree = data_manager.get_tree()
    return jsonify(tree)


@app.route('/node', methods=['POST'])
def node_create(data_manager: DataManager):
    data = request.get_json()
    data_manager.create_node(data['path'])
    return Response()


@app.route('/node', methods=['PUT'])
def node_rename(data_manager: DataManager):
    data = request.get_json()
    data_manager.rename_node(data['old_path'], data['new_path'])
    return Response()


@app.route('/node', methods=['DELETE'])
def node_delete(data_manager: DataManager):
    data = request.get_json()
    data_manager.delete_node(data['path'])
    return Response()


def configure_dependencies():

    def configure(binder):
        binder.bind(
            DataManager,
            to=DataManager.create_from_environ(),
            scope=flask_injector.request
        )

    FlaskInjector(app=app, modules=[configure])


if __name__ == '__main__':
    configure_dependencies()
    app.run(debug=True)
