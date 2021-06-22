from mementoweb.validator.errors.header_errors import HeaderTypeNotFoundError
from mementoweb.validator.errors.uri_errors import HttpConnectionFailError, InvalidUriError, HttpRequestFailError
from mementoweb.validator.http import HttpConnection, http
from mementoweb.validator.tests.test import BaseTest, TestResult
from mementoweb.validator.tests.test import TestReport


class MementoRedirectTestReport(TestReport):
    connection: HttpConnection = None

    def __init__(self, connection: HttpConnection = None, *args, **kwargs):
        super(MementoRedirectTestReport, self).__init__(*args, **kwargs)
        self.connection = connection


class MementoRedirectTest(BaseTest):
    MISSING_REDIRECTION_LOCATION: str = "Missing location for redirection"

    REDIRECTION_BEFORE_MEMENTO: str = "Redirection before memento"

    BROKEN_REDIRECTION: str = "Redirection URI broken"

    VALID_MEMENTO_STATUS: str = "Memento contains status 200, 204, or 206"

    INVALID_MEMENTO_STATUS: str = "Memento does not contain status 200, 204, or 206"

    _description = "Tests for the memento redirection. Checks for any redirection and tests for the validity"

    _test_report: MementoRedirectTestReport

    def __init__(self):
        super().__init__()
        self._test_report = MementoRedirectTestReport(
            name=self._name(),
            description=self._description,
            report_status=TestReport.REPORT_FAIL,
            tests=[],
            connection=None
        )

    def test(self, connection: HttpConnection) -> MementoRedirectTestReport:
        self._test_report.connection = connection
        response_status: int = connection.get_response().status
        while 300 <= response_status < 400:

            try:
                redirect_location = connection.get_headers("location")
                connection = http(redirect_location)
                response_status = connection.get_response().status
                self.add_test_result(
                    TestResult(name=MementoRedirectTest.REDIRECTION_BEFORE_MEMENTO, status=TestResult.TEST_WARN))
                self._test_report.connection = connection

            except HeaderTypeNotFoundError:
                self.add_test_result(TestResult(name=MementoRedirectTest.MISSING_REDIRECTION_LOCATION))
                break

            except (InvalidUriError, HttpRequestFailError, HttpConnectionFailError):
                self.add_test_result(TestResult(name=MementoRedirectTest.BROKEN_REDIRECTION))
                break

        else:
            if response_status in [200, 204, 206]:
                self.add_test_result(TestResult(name=MementoRedirectTest.VALID_MEMENTO_STATUS, status=TestResult.TEST_PASS))
                self._test_report.report_status = TestReport.REPORT_PASS
            else:
                self.add_test_result(TestResult(MementoRedirectTest.INVALID_MEMENTO_STATUS))

        return self._test_report
