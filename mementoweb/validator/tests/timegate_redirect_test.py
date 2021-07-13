from typing_extensions import Literal

from mementoweb.validator.errors.header_errors import HeaderTypeNotFoundError, HeadersNotFoundError, HeaderParseError, \
    LinkHeaderNotFoundError
from mementoweb.validator.errors.uri_errors import HttpRequestFailError, InvalidUriError, HttpConnectionFailError
from mementoweb.validator.http import http, HttpConnection
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

    TIMEGATE_FUTURE_RETURN_302 = "TimeGate returns 302 for datetime in future"

    TIMEGATE_FUTURE_INVALID_RETURN = "Timegate does not return 302 for datetime in future"

    TIMEGATE_PAST_RETURN_302 = "TimeGate returns 302 for datetime in past"

    TIMEGATE_PAST_INVALID_RETURN = "Timegate does not return 302 for datetime in past"

    TIMEGATE_BROKEN_RETURN_400 = "TimeGate returns 400 for broken datetime"

    TIMEGATE_BROKEN_INVALID_RETURN = "Timegate does not return 400 for broken datetime"

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
             datetime: str,
             test_type=Literal["future", "past", "broken", "normal", "blank"],
             assert_connection: HttpConnection = None
             ) -> TimeGateRedirectTestReport:
        """

        :param connection: Primary connection for testing the redirection
        :param datetime: Datetime used for establishing the primary connection. Should conform the standard specification
        :param test_type: Test type to perform from "normal" (or ""), "future", "past", "broken" defaults to "normal" (or "")
        :param assert_connection: Secondary connection for validating memento information. Ignored when test_type is "normal" or ""
        :return:
        """

        if test_type is None:
            test_type = "normal"
        self._test_report.connection = connection

        if test_type == "future":
            return self._future(assert_connection)
        elif test_type == "past":
            return self._past(assert_connection)
        elif test_type == "broken":
            return self._broken(assert_connection)
        elif test_type == "blank":
            return self._blank(assert_connection)
        else:
            return self._normal(connection, datetime)

    def _broken(self, assert_connection):
        self._test_report.name += "-broken"

        response_status: int = assert_connection.get_response().status

        if response_status != 400:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_BROKEN_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_BROKEN_RETURN_400,
                                            status=TestResult.TEST_PASS))
        return self._test_report

    def _past(self, assert_connection: HttpConnection = None
              ) -> TimeGateRedirectTestReport:

        self._test_report.name += "-past"

        response = assert_connection.get_response()
        response_status: int = response.status

        if response_status != 302:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_PAST_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_PAST_RETURN_302,
                                            status=TestResult.TEST_PASS))

            mementos = assert_connection.get_response().search_link_headers("memento")
        # TODO sort mementos and check

        return self._test_report

    def _future(self, assert_connection: HttpConnection = None
                ) -> TimeGateRedirectTestReport:

        self._test_report.name += "-future"

        response = assert_connection.get_response()
        response_status: int = response.status

        if response_status != 302:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_FUTURE_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_FUTURE_RETURN_302,
                                            status=TestResult.TEST_PASS))

            mementos = assert_connection.get_response().search_link_headers("memento")
            # TODO sort mementos and check

        return self._test_report

    def _normal(self, connection: HttpConnection,
                datetime: str,
                ) -> TimeGateRedirectTestReport:

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
            except (HeadersNotFoundError, HeaderTypeNotFoundError, HeaderParseError, LinkHeaderNotFoundError):
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

    def _blank(self, assert_connection):
        self._test_report.name += "-blank"

        response = assert_connection.get_response()
        response_status: int = response.status

        if response_status != 302:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_FUTURE_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_FUTURE_RETURN_302,
                                            status=TestResult.TEST_PASS))

            # mementos = assert_connection.get_response().search_link_headers("memento")
            # TODO sort mementos and check

        return self._test_report