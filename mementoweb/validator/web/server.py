import os

from dotenv import dotenv_values
from flask import Flask, jsonify, send_from_directory

from mementoweb.validator.web.main_controller import MainController

app = Flask(__name__, static_folder='', static_url_path='')

config = dotenv_values("web-validator.env")


@app.route("/docs/", defaults={'path': 'index.html'})
@app.route("/docs/<path:path>")
def docs(path):
    return send_from_directory(os.getcwd() + config.get("docs-dir", "/static/docs/"), path)


@app.route("/api-docs/", defaults={'path': 'index.html'})
@app.route("/api-docs/<path:path>")
def api_docs(path):
    return send_from_directory(os.getcwd() + config.get("api-docs-dir", "/static/api-docs/"), path)


@app.route("/app/", defaults={'path': "index.html"})
@app.route("/app/<path:path>")
def webapp_static(path):
    return send_from_directory(os.getcwd() + config.get("app-dir", "/static/app/"), path)


@app.route("/")
def main():
    controller = MainController()
    return jsonify(controller.main())
