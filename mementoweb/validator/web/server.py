from flask import Flask, request, jsonify
from typing_extensions import TypedDict

from mementoweb.validator.config import Config
from mementoweb.validator.pipelines.timegate import TimeGate
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timemap import TimeMap

app = Flask(__name__)

# TODO : transfer web server configuration to env file
#  Add endpoint to serve html page??
Config.file_path = "config.xml"


@app.route("/original")
def original():
    return _handle_request(Original())


@app.route("/timegate")
def timegate():
    return _handle_request(TimeGate())


@app.route("/memento")
def memento():
    return _handle_request(Memento())


@app.route("/timemap")
def timemap():
    return _handle_request(TimeMap())


def _handle_request(pipeline):
    uri = request.args.get("uri")

    errors: [RequestError] = []

    if not uri:
        errors.append({
            "type": "missing parameters",
            "description": "URI missing"
        })
    datetime = request.args.get("datetime")

    if not datetime:
        errors.append({
            "type": "missing parameters",
            "description": "Datetime missing"
        })

    if not len(errors) == 0:
        return {
            "errors": errors
        }

    return jsonify({
        "type": "timegate",
        "uri": uri,
        "datetime": datetime,
        "pipeline": pipeline.name(),
        "results": pipeline.validate(uri)
    })


class RequestError(TypedDict):
    type: str

    description: str
