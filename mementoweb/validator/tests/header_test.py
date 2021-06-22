from mementoweb.validator.errors.header_errors import LinkHeaderNotFoundError, HeadersNotFoundError
from mementoweb.validator.http import HttpConnection
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class HeaderTest(BaseTest):
    LINK_HEADER_NOT_PRESENT = "Link Header not present"

    HEADERS_NOT_PRESENT = "Headers not present"

    TIMEGATE_NOT_PRESENT = "Timegate link not present"

    TIMEBUNDLE_NOT_PRESENT = "Timebundle link not present"

    TIMEMAP_NOT_PRESENT = "Timemap link not present"

    TIMEGATE_PRESENT = "Timegate link present"

    TIMEBUNDLE_PRESENT = "Timebundle link present"

    TIMEMAP_PRESENT = "Timemap link present"

    def test(self, connection: HttpConnection) -> TestReport:

        try:
            self._test_report.report_status = TestReport.REPORT_PASS

            if not len(connection.search_link_headers("timegate")):
                self.add_test_result(TestResult(description=HeaderTest.TIMEGATE_NOT_PRESENT))
                self._test_report.report_status = TestReport.REPORT_FAIL
            else:
                self.add_test_result(TestResult(description=HeaderTest.TIMEGATE_PRESENT, status=TestResult.TEST_PASS))

            if not len(connection.search_link_headers("timebundle")):
                self.add_test_result(TestResult(description=HeaderTest.TIMEBUNDLE_NOT_PRESENT))
                self._test_report.report_status = TestReport.REPORT_FAIL
            else:
                self.add_test_result(TestResult(description=HeaderTest.TIMEBUNDLE_PRESENT, status=TestResult.TEST_PASS))

            if not len(connection.search_link_headers("timemap")):
                self.add_test_result(TestResult(description=HeaderTest.TIMEMAP_NOT_PRESENT))
                self._test_report.report_status = TestReport.REPORT_FAIL
            else:
                self.add_test_result(TestResult(description=HeaderTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))

        except LinkHeaderNotFoundError:
            self._test_report.report_status = TestReport.REPORT_FAIL
            self.add_test_result(TestResult(description=HeaderTest.LINK_HEADER_NOT_PRESENT))

        except HeadersNotFoundError:
            self._test_report.report_status = TestReport.REPORT_FAIL
            self.add_test_result(TestResult(description=HeaderTest.HEADERS_NOT_PRESENT))

        return self._test_report

