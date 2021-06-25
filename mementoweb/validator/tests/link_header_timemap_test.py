from mementoweb.validator.http import HttpResponse
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.test import TestReport, TestResult


class LinkHeaderTimeMapTest(LinkHeaderTest):

    TIMEMAP_PRESENT = "Timemap link present"

    TIMEMAP_TYPE_PRESENT = "Timemap type present"

    TIMEMAP_TYPE_NOT_PRESENT = "Timemap type not present"

    def _test_memento(self, response: HttpResponse) -> TestReport:

        timemaps = response.search_link_headers("timemap")

        if not len(timemaps):
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEMAP_NOT_PRESENT, status=TestResult.TEST_WARN))
            self._test_report.report_status = TestReport.REPORT_WARN
        else:
            self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))
            timemap: dict
            for timemap in timemaps:
                # TODO : add matching content type
                if "type" in timemap.keys() and timemap["type"] == "application/link-format":
                    self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_TYPE_PRESENT,
                                                    status=TestResult.TEST_PASS))
                else:
                    self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_TYPE_NOT_PRESENT))

        return self._test_report

    def _test_original(self, response: HttpResponse) -> TestReport:
        if not len(response.search_link_headers("timemap")):
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEMAP_NOT_PRESENT))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS

        return self._test_report
