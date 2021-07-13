from typing_extensions import TypedDict

from flask import request

from mementoweb.validator.pipelines import TimeGate
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timemap import TimeMap
from mementoweb.validator.tests.timegate_redirect_test import TimeGateRedirectTest, TimeGateRedirectTestReport


def _get_validator(validator_type: str):
    if validator_type == "original":
        return Original()
    elif validator_type == "memento":
        return Memento()
    elif validator_type == "timemap":
        return TimeMap()
    elif validator_type == "timegate":
        return TimeGate()
    return None


class MainController:

    def main():
        errors: [RequestError] = []

        request_type = request.args.get("type")
        validator = _get_validator(request_type)

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

        dict_reports = {report.name: report for report in reports}
        time_gate_report: TimeGateRedirectTestReport = dict_reports.get(TimeGateRedirectTest()._name())


        print("test")
        return {
            "type": request_type,
            "uri": uri,
            "datetime": datetime,
            "pipeline": validator.name(),
            "results": [report.to_json() for report in reports]
        }


class RequestError(TypedDict):
    type: str

    description: str
