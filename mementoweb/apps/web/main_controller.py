from flask import request
from typing_extensions import TypedDict

from mementoweb.validator.pipelines import TimeGate
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timemap import TimeMap


def _get_boolean_args(param, default=False):
    if not request.args.get(param):
        return default
    else:
        if request.args.get(param).lower() == 'true':
            return True

    return False


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

        follow = _get_boolean_args("followLinks")

        full_tm_check = _get_boolean_args("fullTMCheck")

        if request_type == "timegate":
            return self._handle_timegate(uri, datetime, follow, full_tm_check)
        elif request_type == "memento":
            return self._handle_memento(uri, datetime, follow, full_tm_check)
        elif request_type == "timemap":
            return self._handle_timemap(uri, datetime, follow, full_tm_check)
        elif request_type == "original":
            return self._handle_original(uri, datetime, follow, full_tm_check)
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

    def _handle_memento(self, uri, datetime, follow, full_tm_check):
        result = self._memento.validate(uri, datetime)

        follow_tests = dict()
        if follow:
            follow_tests['timegate'] = [self._follow_timegate(timegate, datetime) for timegate in result.timegates]

            follow_tests['timemap'] = [self._follow_timemap(timemap, datetime, full_tm_check) for timemap in result.timemaps]

        return {
            "type": "memento",
            "uri": uri,
            "datetime": datetime,
            "pipeline": self._memento.name(),
            "result": result.to_json(),
            "follow": follow_tests
        }

    def _handle_timegate(self, uri, datetime, follow, full_tm_check):

        result = self._timegate.validate(uri, datetime)

        follow_tests = dict()
        if follow:
            follow_tests['memento'] = [self._follow_memento(memento, datetime) for memento in result.mementos]

            follow_tests['timemap'] = [self._follow_timemap(timemap, datetime, full_tm_check) for timemap in result.timemaps]

        return {
            "type": "timegate",
            "uri": uri,
            "datetime": datetime,
            "pipeline": self._timegate.name(),
            "result": result.to_json(),
            "follow": follow_tests
        }

    def _handle_timemap(self, uri, datetime, follow, full_tm_check):
        result = self._timemap.validate(uri, datetime, full=full_tm_check)

        return {
            "type": "timemap",
            "uri": uri,
            "datetime": datetime,
            "pipeline": self._timegate.name(),
            "result": result.to_json()
        }

    def _handle_original(self, uri, datetime, follow, full_tm_check):
        result = Original().validate(uri, datetime)

        follow_tests = dict()
        if follow:
            follow_tests['timegate'] = [self._follow_timegate(timegate, datetime) for timegate in result.timegates]

            follow_tests['timemap'] = [self._follow_timemap(timemap, datetime, full_tm_check) for timemap in result.timemaps]

        return {
            "type": "original",
            "uri": uri,
            "datetime": datetime,
            "pipeline": Original().name(),
            "result": result.to_json(),
            "follow": follow_tests
        }

    def _follow_timemap(self, timemap, datetime, full_tm_check):
        return {"uri": timemap,
                "datetime": datetime,
                "result": TimeMap().validate(timemap, datetime, full=full_tm_check).to_json()}

    def _follow_timegate(self, timemap, datetime):
        return {"uri": timemap,
                "datetime": datetime,
                "result": TimeGate().validate(timemap, datetime).to_json()}

    def _follow_memento(self, timemap, datetime):
        return {"uri": timemap,
                "datetime": datetime,
                "result": Memento().validate(timemap, datetime).to_json()}


class RequestError(TypedDict):
    type: str

    description: str