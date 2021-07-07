from flask import Flask, request, jsonify, send_from_directory
from typing_extensions import TypedDict

from mementoweb.validator.config import Config
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timegate import TimeGate
from mementoweb.validator.pipelines.timemap import TimeMap

app = Flask(__name__, static_folder='', static_url_path='')

# TODO : transfer web server configuration to env file
#  Add endpoint to serve html page??
Config.file_path = "config.xml"


@app.route("/docs/<path:path>")
def docs(path):
    return send_from_directory('../../../docs/build/html/', path)


@app.route("/")
def main():
    errors: [RequestError] = []

    validator = None
    request_type = request.args.get("type")

    if request_type == "original":
        validator = Original()
    elif request_type == "memento":
        validator = Memento()
    elif request_type == "timemap":
        validator = TimeMap()
    elif request_type == "timegate":
        validator = TimeGate()

    uri = request.args.get("uri")
    if not request_type:
        errors.append({
            "type": "missing parameters",
            "description": "Type missing"
        })
    elif validator is None:
        errors.append({
            "type": "invalid parameters",
            "description": "Type invalid"
        })

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
    reports = validator.validate(uri)
    return jsonify({
        "type": request_type,
        "uri": uri,
        "datetime": datetime,
        "pipeline": validator.name(),
        "results": [report.to_json() for report in reports]
    })


class RequestError(TypedDict):
    type: str

    description: str
