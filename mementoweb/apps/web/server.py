#
#  Copyright (c) 2021. Los Alamos National Laboratory (LANL).
#  Written by: Bhanuka Mahanama (bhanuka@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  Correspondence: Lyudmila Balakireva, PhD (ludab@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  See LICENSE in the project root for license information.
#

import os

from dotenv import dotenv_values
from flask import Flask, jsonify, send_from_directory

from mementoweb.apps.web.main_controller import MainController

app = Flask(__name__, static_folder='', static_url_path='')

config = dotenv_values("web-validator.env")


@app.route("/docs/", defaults={'path': 'index.html'})
@app.route("/docs/<path:path>")
def docs(path):
    return send_from_directory(os.getcwd() + config.get("docs-dir", "/static/docs/"), path)


@app.route("/api")
def main():
    controller = MainController()
    return jsonify(controller.main())


@app.route("/", defaults={'path': 'index.html'})
@app.route("/app/", defaults={'path': "index.html"})
@app.route("/app/<path:path>")
def webapp_static(path):
    return send_from_directory(os.getcwd() + config.get("app-dir", "/static/app/"), path)
