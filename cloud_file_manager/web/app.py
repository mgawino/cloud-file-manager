import flask_injector
from flask_injector import FlaskInjector
from flask import Flask, render_template, jsonify, send_from_directory, Response

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
def node_create():
    return Response()


@app.route('/node', methods=['PUT'])
def node_rename():
    return Response()


@app.route('/node', methods=['DELETE'])
def node_delete():
    return Response()


def configure_dependencies():

    def configure(binder):
        binder.bind(
            DataManager,
            to=DataManager.from_environ_config(),
            scope=flask_injector.request
        )

    FlaskInjector(app=app, modules=[configure])


if __name__ == '__main__':
    configure_dependencies()
    app.run(debug=True)
