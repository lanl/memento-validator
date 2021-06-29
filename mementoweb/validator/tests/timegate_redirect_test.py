from mementoweb.validator.errors.header_errors import HeaderTypeNotFoundError, HeadersNotFoundError, HeaderParseError
from mementoweb.validator.errors.uri_errors import HttpRequestFailError, InvalidUriError, HttpConnectionFailError
from mementoweb.validator.http import HttpResponse, http, HttpConnection
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class TimeGateRedirectTestReport(TestReport):
    connection: HttpConnection = None

    def __init__(self, connection: HttpConnection = None, *args, **kwargs):
        super(TimeGateRedirectTestReport, self).__init__(*args, **kwargs)
        self.connection = connection


class TimeGateRedirectTest(BaseTest):
    MISSING_REDIRECTION_LOCATION = "Missing location for redirection"

    REDIRECTION_MISSING_ORIGINAL = "Redirection to another timegate"

    REDIRECTION_BEFORE_TIMEGATE = "Redirection before timegate"

    BROKEN_REDIRECTION = "Redirection URI broken"

    TIMEGATE_RETURN_302 = "TimeGate returns 302"

    TIMEGATE_RETURN_200 = "TimeGate returns 200"

    TIMEGATE_RETURN_INVALID_STATUS = "TimeGate does not return 302/ 200"

    _description = "Tests for the timegate redirection. Checks for any redirection and tests for the validity"

    _test_report: TimeGateRedirectTestReport

    def __init__(self):
        super().__init__()
        self._test_report = TimeGateRedirectTestReport(
            name=self._name(),
            description=self._description,
            report_status=TestReport.REPORT_FAIL,
            tests=[],
            connection=None
        )

    def test(self, connection: HttpConnection,
             datetime) -> TimeGateRedirectTestReport:
        self._test_report.connection = connection

        response = connection.get_response()
        response_status: int = response.status
        try:
            vary = response.get_headers('Vary')
        except HeaderTypeNotFoundError:
            vary = ''

        while 300 <= response_status < 400 and not vary:

            # Check for link rel original
            try:
                original_uri = response.search_link_headers("original")
                self.add_test_result(TestResult(name=TimeGateRedirectTest.REDIRECTION_MISSING_ORIGINAL,
                                                status=TestResult.TEST_PASS))
            except (HeadersNotFoundError, HeaderTypeNotFoundError, HeaderParseError):
                # Modify test result or description
                self.add_test_result(TestResult(name=TimeGateRedirectTest.REDIRECTION_MISSING_ORIGINAL,
                                                status=TestResult.TEST_WARN))

            # Check and test redirection location
            try:
                redirect_location = response.get_headers("location")
                connection = http(redirect_location, datetime=datetime)
                response_status = connection.get_response().status
                self.add_test_result(
                    TestResult(name=TimeGateRedirectTest.REDIRECTION_BEFORE_TIMEGATE, status=TestResult.TEST_PASS))
                self._test_report.connection = connection
                response = connection.get_response()

            except HeaderTypeNotFoundError:
                self.add_test_result(TestResult(name=TimeGateRedirectTest.MISSING_REDIRECTION_LOCATION))
                break

            except (InvalidUriError, HttpRequestFailError, HttpConnectionFailError):
                self.add_test_result(TestResult(name=TimeGateRedirectTest.BROKEN_REDIRECTION))
                break

            response_status = response.status

        if response_status == 302:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_RETURN_302, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS
        elif response_status == 200:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_RETURN_200, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS
        else:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_RETURN_INVALID_STATUS,
                                            status=TestResult.TEST_FAIL))

        return self._test_report
