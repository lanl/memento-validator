from mementoweb.validator.errors.header_errors import HeadersNotFoundError, HeaderTypeNotFoundError
from mementoweb.validator.http import HttpConnection
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class ContentNegotiationTest(BaseTest):

    HEADERS_NOT_PRESENT = "Headers not present"

    CONTENT_NEGOTIATION_HEADERS_NOT_PRESENT = "Resource does not support content negotiation"

    CONTENT_NEGOTIATION_HEADERS_PRESENT = "Resource supports content negotiation"

    def test(self, connection: HttpConnection) -> TestReport:

        self._test_report.report_status = TestReport.REPORT_WARN

        try:
            memento_headers = connection.get_headers("Memento-Datetime")
            self._test_report.report_status = TestReport.REPORT_PASS
            self.add_test_result(TestResult(name=ContentNegotiationTest.CONTENT_NEGOTIATION_HEADERS_PRESENT,
                                            status=TestResult.TEST_PASS))
        except HeadersNotFoundError:
            self.add_test_result(TestResult(name=ContentNegotiationTest.HEADERS_NOT_PRESENT))
        except HeaderTypeNotFoundError:
            self.add_test_result(TestResult(name=ContentNegotiationTest.CONTENT_NEGOTIATION_HEADERS_NOT_PRESENT))

        return self._test_report

