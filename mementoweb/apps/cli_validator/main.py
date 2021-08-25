from mementoweb.validator.pipelines import TimeGate
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timemap import TimeMap


class CliHandler:

    _original: Original

    _memento: Memento

    _timemap: TimeMap

    _timegate: TimeGate

    def __init__(self):
        self._original = Original()
        self._memento = Memento()
        self._timemap = TimeMap()
        self._timegate = TimeGate()

    def handle_timegate(self, uri, datetime, follow, full_tm_check):
        result = self._timegate.validate(uri, datetime)

        follow_tests = dict()
        if follow:
            follow_tests['memento'] = [self._follow_memento(memento, datetime) for memento in result.mementos]

            follow_tests['timemap'] = [self._follow_timemap(timemap, datetime, full_tm_check) for timemap in
                                       result.timemaps]

        return {
            "type": "timegate",
            "uri": uri,
            "datetime": datetime,
            "pipeline": self._timegate.name(),
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


def run(uri, resource_type, datetime, follow):
    print(resource_type)
    cli_handler = CliHandler()

    if resource_type == "timegate":
        print("here")
        return cli_handler.handle_timegate(uri, datetime, follow=follow, full_tm_check=True)
