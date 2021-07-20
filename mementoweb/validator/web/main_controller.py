from flask import request
from typing_extensions import TypedDict

from mementoweb.validator.pipelines import TimeGate
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timemap import TimeMap


class MainController:

    _original: Original

    _memento: Memento

    _timemap: TimeMap

    _timegate: TimeGate

    def __init__(self):
        self._original = Original()
        self._memento = Memento()
        self._timemap = TimeMap()
        self._timegate = TimeGate()

    def main(self):
        errors: [RequestError] = []

        request_type = request.args.get("type")

        uri = request.args.get("uri")
        if not request_type:
            errors.append({
                "type": "missing parameters",
                "description": "Type missing"
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

        if request_type == "timegate":
            return self._handle_timegate(uri, datetime)
        elif request_type == "memento":
            return self._handle_memento(uri, datetime)
        elif request_type == "timemap":
            return self._handle_timemap(uri, datetime)
        elif request_type == "original":
            return self._handle_original(uri, datetime)
        else:
            errors.append({
                "type": "invalid parameters",
                "description": "Type invalid"
            })

        return {
            "errors": errors
        }
        # dict_reports = {report.name: report for report in reports}
        # time_gate_report: TimeGateRedirectTestReport = dict_reports.get(TimeGateRedirectTest()._name())
        #
        #
        # print("test")
        # return {
        #     "type": request_type,
        #     "uri": uri,
        #     "datetime": datetime,
        #     "pipeline": validator.name(),
        #     "results": [report.to_json() for report in reports]
        # }

    def _handle_memento(self, uri, datetime):
        result = self._memento.validate(uri, datetime)

        return {
            "type": "memento",
            "uri": uri,
            "datetime": datetime,
            "pipeline": self._timegate.name(),
            "result": result.to_json()
        }

    def _handle_timegate(self, uri, datetime):

        result = self._timegate.validate(uri, datetime)

        follow = request.args.get("followLinks") or False

        follow_tests = dict()
        if follow:
            follow_tests['memento'] = [{"uri": memento,
                                        "datetime": datetime,
                                        "result": self._memento.validate(memento, datetime).to_json()}
                                       for memento in result.mementos]

            follow_tests['timemap'] = [{"uri": timemap,
                                        "datetime": datetime,
                                        "result": self._memento.validate(timemap, datetime).to_json()}
                                       for timemap in result.timemaps]

        return {
            "type": "timegate",
            "uri": uri,
            "datetime": datetime,
            "pipeline": self._timegate.name(),
            "result": result.to_json(),
            "follow": follow_tests
        }

    def _handle_timemap(self, uri, datetime):
        result = self._timemap.validate(uri, datetime)

        return {
            "type": "timemap",
            "uri": uri,
            "datetime": datetime,
            "pipeline": self._timegate.name(),
            "result": result.to_json()
        }

    def _handle_original(self, uri, datetime):
        result = Original().validate(uri, datetime)

        follow = request.args.get("followLinks")

        follow_tests = dict()
        if follow == 'true':
            follow_tests['timegate'] = [{"uri": timegate,
                                         "datetime": datetime,
                                         "result": TimeGate().validate(timegate, datetime).to_json()}
                                        for timegate in result.timegates]

            follow_tests['timemap'] = [{"uri": timemap,
                                        "datetime": datetime,
                                        "result": TimeMap().validate(timemap, datetime).to_json()}
                                       for timemap in result.timemaps]

        return {
            "type": "original",
            "uri": uri,
            "datetime": datetime,
            "pipeline": Original().name(),
            "result": result.to_json(),
            "follow": follow_tests
        }


class RequestError(TypedDict):
    type: str

    description: str
