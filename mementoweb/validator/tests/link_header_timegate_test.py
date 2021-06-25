from mementoweb.validator.http import HttpResponse
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.test import TestReport, TestResult


class LinkHeaderTimeGateTest(LinkHeaderTest):

    TIMEGATE_PRESENT = "Timegate link present"

    TIMEGATE_NOT_PRESENT = "Timegate link present"

    def _test_original(self, response: HttpResponse) -> TestReport:
        self._test_report.report_status = TestReport.REPORT_PASS

        if not len(response.search_link_headers("timegate")):
            self.add_test_result(TestResult(name=LinkHeaderTimeGateTest.TIMEGATE_NOT_PRESENT,
                                            status=TestResult.TEST_FAIL))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTimeGateTest.TIMEGATE_PRESENT, status=TestResult.TEST_PASS))

        return self._test_report


