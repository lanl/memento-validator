import os

from flask import Flask, request, jsonify, send_from_directory
from typing_extensions import TypedDict

from mementoweb.validator.config import Config
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timegate import TimeGate
from mementoweb.validator.pipelines.timemap import TimeMap
from mementoweb.validator.web.main_controller import MainController

app = Flask(__name__, static_folder='', static_url_path='')

# TODO : transfer web server configuration to env file
#  Add endpoint to serve html page??
Config.file_path = "config.xml"


@app.route("/docs/", defaults={'path': 'index.html'})
@app.route("/docs/<path:path>")
def docs(path):
    # return send_from_directory('../../../docs/build/html/', path)
    return send_from_directory(os.getcwd() + "/static/docs/", path)


@app.route("/app/", defaults={'path': "index.html"})
@app.route("/app/<path:path>")
def webapp_static(path):
    # return send_from_directory('../../../web-validator/dist/', path)
    return send_from_directory(os.getcwd() + '/static/app/', path)


@app.route("/")
def main():
    return jsonify(MainController.main())
