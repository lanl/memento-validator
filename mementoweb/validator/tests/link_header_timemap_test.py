from typing import List

from mementoweb.validator.http import HttpResponse
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.test import TestReport, TestResult


class LinkHeaderTimeMapTestReport(TestReport):
    time_map_uris: List[str] = []

    def __init__(self, time_map_uris=None, *args, **kwargs):
        super(LinkHeaderTimeMapTestReport, self).__init__(*args, **kwargs)
        if time_map_uris is None:
            time_map_uris = []
        self.time_map_uris = time_map_uris


class LinkHeaderTimeMapTest(LinkHeaderTest):
    TIMEMAP_PRESENT = "Timemap link present"

    TIMEMAP_NOT_PRESENT = "Timemap link not present"

    TIMEMAP_TYPE_PRESENT = "Timemap type present"

    TIMEMAP_TYPE_NOT_PRESENT = "Timemap type not present"

    _test_report: LinkHeaderTimeMapTestReport

    def __init__(self):
        super().__init__()
        self._test_report = LinkHeaderTimeMapTestReport(
            name=self._name(),
            description=self._description,
            report_status=TestReport.REPORT_FAIL,
            tests=[],
            time_map_uris=[]
        )

    def _test_timegate(self, response: HttpResponse) -> LinkHeaderTimeMapTestReport:
        self._test_report.report_status = TestReport.REPORT_PASS
        timemaps = response.search_link_headers('timemap')
        if not timemaps:
            self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_NOT_PRESENT,
                                            status=TestResult.TEST_WARN))
        else:
            self.add_test_result(TestResult(LinkHeaderTimeMapTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))

            for timemap in timemaps:
                if timemap['type'] == "application/link-format":
                    self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_TYPE_PRESENT,
                                                    status=TestResult.TEST_PASS))
                    self._test_report.time_map_uris.append(timemap['link'])

            if not self._test_report.time_map_uris:
                # We dont have any valid time map uris -> Fail the report
                self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_TYPE_NOT_PRESENT,
                                                status=TestResult.TEST_FAIL))
                self._test_report.report_status = TestReport.REPORT_FAIL

        return self._test_report

    def _test_memento(self, response: HttpResponse) -> TestReport:

        timemaps = response.search_link_headers("timemap")

        if not len(timemaps):
            self.add_test_result(
                TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_NOT_PRESENT, status=TestResult.TEST_WARN))
            self._test_report.report_status = TestReport.REPORT_WARN
        else:
            self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))
            timemap: dict
            for timemap in timemaps:
                # TODO : add matching content type
                if "type" in timemap.keys() and timemap["type"] == "application/link-format":
                    self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_TYPE_PRESENT,
                                                    status=TestResult.TEST_PASS))
                    self._test_report.report_status = TestReport.REPORT_PASS
                else:
                    self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_TYPE_NOT_PRESENT))

        return self._test_report

    def _test_original(self, response: HttpResponse) -> TestReport:
        if not len(response.search_link_headers("timemap")):
            self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_NOT_PRESENT))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS

        return self._test_report
