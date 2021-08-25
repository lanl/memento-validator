from mementoweb.validator.errors.header_errors import HeadersNotFoundError, HeaderTypeNotFoundError
from mementoweb.validator.util.http import HttpResponse
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult

"""
    Tests for content negotiation using the Memento-Datetime header.
"""


class DatetimeNegotiationTest(BaseTest):

    _description = "Tests for the Datetime negotiation capabilities using through Memento-Datetime headers."

    HEADERS_NOT_PRESENT = "Response headers not present"

    CONTENT_NEGOTIATION_HEADERS_NOT_PRESENT = "Resource does not support datetime negotiation"

    CONTENT_NEGOTIATION_HEADERS_PRESENT = "Resource supports datetime negotiation"

    def __init__(self):
        super(DatetimeNegotiationTest, self).__init__()

    def test(self, response: HttpResponse) -> TestReport:

        self._test_report.report_status = TestReport.REPORT_WARN

        try:
            memento_headers = response.get_headers("Memento-Datetime")
            self._test_report.report_status = TestReport.REPORT_PASS
            self.add_test_result(TestResult(name=DatetimeNegotiationTest.CONTENT_NEGOTIATION_HEADERS_PRESENT,
                                            status=TestResult.TEST_PASS))
        except HeadersNotFoundError:
            self.add_test_result(TestResult(name=DatetimeNegotiationTest.HEADERS_NOT_PRESENT))
        except HeaderTypeNotFoundError:
            self.add_test_result(TestResult(name=DatetimeNegotiationTest.CONTENT_NEGOTIATION_HEADERS_NOT_PRESENT))

        return self._test_report
