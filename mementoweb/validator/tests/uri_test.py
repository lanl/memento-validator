from mementoweb.validator.errors.uri_errors import HttpConnectionFailError, InvalidUriError, HttpRequestFailError
from mementoweb.validator.http import HttpConnection, http
from mementoweb.validator.tests.test import BaseTest, TestResult
from mementoweb.validator.tests.test import TestReport


class URITestReport(TestReport):
    connection: HttpConnection = None

    def __init__(self, connection: HttpConnection = None, *args, **kwargs):
        super(URITestReport, self).__init__(*args, **kwargs)
        self.connection = connection


"""
    Performs URI validation and connectivity test for a given URI.
"""


class URITest(BaseTest):
    VALID_URI: str = "Valid URI"

    INVALID_URI: str = "Invalid URI"

    REQUEST_FAIL: str = "HTTP(s) Request Failed"

    CONNECTION_FAIL: str = "Could not connect to URI"

    _description = "Tests for the validity of the URI of the resource including validity and connectivity"

    _test_report: URITestReport

    def __init__(self):
        super().__init__()
        self._test_report = URITestReport(
            name=self._name(),
            description=self._description,
            report_status=TestReport.REPORT_FAIL,
            tests=[],
            connection=None
        )

    def test(self, uri: str, datetime: str) -> URITestReport:

        try:
            connection: HttpConnection = http(uri, datetime=datetime)
            self._test_report.connection = connection
            self._test_report.report_status = TestReport.REPORT_PASS
            self.add_test_result(TestResult(name=URITest.VALID_URI, status=TestResult.TEST_PASS))
        except InvalidUriError:
            self.add_test_result(TestResult(name=URITest.INVALID_URI))
        except HttpConnectionFailError:
            self.add_test_result(TestResult(name=URITest.CONNECTION_FAIL))
        except HttpRequestFailError:
            self.add_test_result(TestResult(name=URITest.REQUEST_FAIL))

        return self._test_report
