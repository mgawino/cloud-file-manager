import flask_injector
import os
from flask_injector import FlaskInjector
from flask import Flask, render_template, jsonify, send_from_directory, Response, request

from cloud_file_manager.services.file_manager import FileManager

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tree', methods=['GET'])
def tree(file_manager: FileManager):
    tree = file_manager.get_tree()
    return jsonify(tree)


@app.route('/node', methods=['POST'])
def node_create(file_manager: FileManager):
    data = request.get_json()
    file_manager.create_node(data['path'])
    return Response()


@app.route('/node', methods=['PUT'])
def node_rename(file_manager: FileManager):
    data = request.get_json()
    file_manager.rename_node(data['old_path'], data['new_path'])
    return Response()


@app.route('/node', methods=['DELETE'])
def node_delete(file_manager: FileManager):
    data = request.get_json()
    file_manager.delete_node(data['path'])
    return Response()


def configure_dependencies():

    def configure(binder):
        binder.bind(
            FileManager,
            to=FileManager.create_from_environ(),
            scope=flask_injector.request
        )

    FlaskInjector(app=app, modules=[configure])


if __name__ == '__main__':
    configure_dependencies()
    app.run(host='0.0.0.0', port=int(os.environ.get('APP_PORT', 5000)))
