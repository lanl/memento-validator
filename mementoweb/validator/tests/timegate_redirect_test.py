#
#  Copyright (c) 2021. Los Alamos National Laboratory (LANL).
#  Written by: Bhanuka Mahanama (bhanuka@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  Correspondence: Lyudmila Balakireva, PhD (ludab@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  See LICENSE in the project root for license information.
#

from dateutil import parser

from mementoweb.validator.errors.header_errors import HeaderTypeNotFoundError, HeadersNotFoundError, HeaderParseError, \
    LinkHeaderNotFoundError
from mementoweb.validator.errors.uri_errors import HttpRequestFailError, InvalidUriError, HttpConnectionFailError
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult
from mementoweb.validator.util.http import http, HttpConnection


class TimeGateRedirectTestReport(TestReport):
    """

        Test report from testing Timegate redirection. Includes updated HTTP connection based on the type of test.

    """
    connection: HttpConnection = None

    def __init__(self, connection: HttpConnection = None, *args, **kwargs):
        super(TimeGateRedirectTestReport, self).__init__(*args, **kwargs)
        self.connection = connection


class TimeGateRedirectTest(BaseTest):
    """

        Implements testing procedures/ variables for testing TimeGate redirection.

    """
    MISSING_REDIRECTION_LOCATION = "Missing location for redirection"

    REDIRECTION_MISSING_ORIGINAL = "Redirection to another timegate"

    REDIRECTION_BEFORE_TIMEGATE = "Redirection before timegate"

    BROKEN_REDIRECTION = "Redirection URI broken"

    TIMEGATE_RETURN_302 = "TimeGate returns 302"

    TIMEGATE_RETURN_307 = "TimeGate returns 307"

    TIMEGATE_RETURN_200 = "TimeGate returns 200"

    TIMEGATE_INVALID_RETURN = "TimeGate does not return 302/ 200"

    REDIRECT_THRESH_PASSED = "Redirect threshold passed"

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

    def test(self, connection: HttpConnection, datetime: str, redirect_threshold: int = 5) -> TimeGateRedirectTestReport:
        """

            Test the redirection of the TimeGate resource provided as a HttpConnection.

        :param connection: Primary connection for testing the redirection
        :param datetime: Datetime used for establishing the primary connection. Should conform the standard specification
        :param redirect_threshold: Maximum number of redirects for warning
        :return: Time gate redirection test report containing results

        """

        self._test_report.connection = connection

        response = connection.get_response()
        response_status: int = response.status
        try:
            vary = response.get_headers('Vary')
        except HeaderTypeNotFoundError:
            vary = ''

        redirect_count = 0

        while 300 <= response_status < 400 and not vary:

            redirect_count = redirect_count + 1

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
                redirect_location = response.get_headers("Location")
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
        if redirect_count >= redirect_threshold:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.REDIRECT_THRESH_PASSED,
                                            status=TestResult.TEST_WARN))

        if response_status == 302:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_RETURN_302, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS
        elif response_status == 200:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_RETURN_200, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS
        elif response_status == 307:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_RETURN_307, status=TestResult.TEST_WARN))
            self._test_report.report_status = TestReport.REPORT_PASS
        else:
            self.add_test_result(TestResult(name=TimeGateRedirectTest.TIMEGATE_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))

        return self._test_report


class TimeGateBlankRedirectTest(TimeGateRedirectTest):

    TIMEGATE_BLANK_VALID_RETURN = "TimeGate returns 200 or redirect for blank Accept-Datetime"

    TIMEGATE_BLANK_INVALID_RETURN = "Timegate does not return 302/200 for blank Accept-Datetime"

    TIMEGATE_BLANK_VALID_REDIRECT = "TimeGate redirects to last memento without Accept-Datetime"

    TIMEGATE_BLANK_INVALID_REDIRECT = "TimeGate does not redirect to last memento without Accept-Datetime"

    def test(self, connection: HttpConnection, datetime: str, redirect_threshold: int = 5) -> TimeGateRedirectTestReport:
        """

            Test the redirection of the TimeGate resource provided as a HttpConnection for compliance with empty
            Accept-Datetime.

        :param connection: Primary connection for testing the redirection
        :param datetime: Ignored
        :param redirect_threshold: Ignored
        :return: Time gate redirection test report containing results

        """

        response = assert_connection.get_response()
        response_status: int = response.status

        if response_status == 302 or response_status == 200:

            self.add_test_result(TestResult(name=TimeGateBlankRedirectTest.TIMEGATE_BLANK_VALID_RETURN,
                                            status=TestResult.TEST_PASS))
            try:
                mementos = response.search_link_headers("memento", regex=True)
                mementos.sort(key=lambda x: parser.parse(x.datetime))
                if len(mementos) > 0:

                    redirect_location = response.get_headers("Location")

                    if redirect_location == mementos[-1].uri:
                        self.add_test_result(TestResult(name=TimeGateBlankRedirectTest.TIMEGATE_BLANK_VALID_REDIRECT,
                                                        status=TestResult.TEST_PASS))
                    else:
                        self.add_test_result(
                            TestResult(name=TimeGateBlankRedirectTest.TIMEGATE_BLANK_INVALID_REDIRECT,
                                       status=TestResult.TEST_WARN))

            except HeaderTypeNotFoundError:
                self.add_test_result(TestResult(name=TimeGateBlankRedirectTest.MISSING_REDIRECTION_LOCATION))

            except parser.ParserError:
                pass

        else:
            self.add_test_result(TestResult(name=TimeGateBlankRedirectTest.TIMEGATE_BLANK_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))

        return self._test_report


class TimeGateBrokenRedirectTest(TimeGateRedirectTest):

    TIMEGATE_BROKEN_VALID_RETURN = "TimeGate returns 400 for broken datetime"

    TIMEGATE_BROKEN_INVALID_RETURN = "Timegate does not return 400 for broken datetime"

    def test(self, connection: HttpConnection, datetime: str, redirect_threshold: int = 5) -> TimeGateRedirectTestReport:
        """

        Test the redirection of the TimeGate resource provided as a HttpConnection for compliance with unparsable
        Accept-Datetime.

        :param connection: Primary connection for testing the redirection
        :param datetime: Ignored
        :param redirect_threshold: Ignored
        :return: Time gate redirection test report containing results

        """

        response_status: int = assert_connection.get_response().status

        if response_status != 400:
            self.add_test_result(TestResult(name=TimeGateBrokenRedirectTest.TIMEGATE_BROKEN_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=TimeGateBrokenRedirectTest.TIMEGATE_BROKEN_VALID_RETURN,
                                            status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS

        return self._test_report


class TimeGatePastRedirectTest(TimeGateRedirectTest):

    TIMEGATE_PAST_VALID_RETURN = "TimeGate returns 302 for datetime in past"

    TIMEGATE_PAST_INVALID_RETURN = "Timegate does not return 302 for datetime in past"

    TIMEGATE_PAST_VALID_REDIRECT = "TimeGate redirects to first memento for datetime in past"

    TIMEGATE_PAST_INVALID_REDIRECT = "TimeGate does not redirect to first memento for datetime in past"

    def test(self, connection: HttpConnection, datetime: str, redirect_threshold: int = 5) -> TimeGateRedirectTestReport:
        """

            Test the redirection of the TimeGate resource provided as a HttpConnection for compliance with
            Accept-Datetime in past (before first memento).

            :param connection: Primary connection for testing the redirection
            :param datetime: Ignored
            :param redirect_threshold: Ignored
            :return: Time gate redirection test report containing results

        """

        response = assert_connection.get_response()
        response_status: int = response.status

        if response_status != 302:
            self.add_test_result(TestResult(name=TimeGatePastRedirectTest.TIMEGATE_PAST_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=TimeGatePastRedirectTest.TIMEGATE_PAST_VALID_RETURN,
                                            status=TestResult.TEST_PASS))

            try:
                mementos = response.search_link_headers("memento", regex=True)
                mementos.sort(key=lambda x: parser.parse(x.datetime))
                if len(mementos) > 0:

                    redirect_location = response.get_headers("Location")

                    if redirect_location == mementos[0].uri:
                        self.add_test_result(TestResult(name=TimeGatePastRedirectTest.TIMEGATE_PAST_VALID_REDIRECT,
                                                        status=TestResult.TEST_PASS))
                    else:
                        self.add_test_result(
                            TestResult(name=TimeGatePastRedirectTest.TIMEGATE_PAST_INVALID_REDIRECT,
                                       status=TestResult.TEST_WARN))

            except HeaderTypeNotFoundError:
                self.add_test_result(TestResult(name=TimeGatePastRedirectTest.MISSING_REDIRECTION_LOCATION))

            except parser.ParserError:
                pass

        return self._test_report


class TimeGateFutureRedirectTest(TimeGateRedirectTest):

    TIMEGATE_FUTURE_VALID_RETURN = "TimeGate returns 302 for datetime in future"

    TIMEGATE_FUTURE_INVALID_RETURN = "Timegate does not return 302 for datetime in future"

    TIMEGATE_FUTURE_VALID_REDIRECT = "TimeGate redirects to first memento for datetime in past"

    TIMEGATE_FUTURE_INVALID_REDIRECT = "TimeGate does not redirect to first memento for datetime in past"

    def test(self, connection: HttpConnection, datetime: str, redirect_threshold: int = 5) -> TimeGateRedirectTestReport:
        """

            Test the redirection of the TimeGate resource provided as a HttpConnection for compliance with
            Accept-Datetime in future.

            :param connection: Primary connection for testing the redirection
            :param datetime: Ignored
            :param redirect_threshold: Ignored
            :return: Time gate redirection test report containing results

        """

        response = assert_connection.get_response()
        response_status: int = response.status

        if response_status != 302:
            self.add_test_result(TestResult(name=TimeGateFutureRedirectTest.TIMEGATE_FUTURE_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=TimeGateFutureRedirectTest.TIMEGATE_FUTURE_VALID_RETURN,
                                            status=TestResult.TEST_PASS))

            try:
                mementos = response.search_link_headers("memento", regex=True)
                mementos.sort(key=lambda x: parser.parse(x.datetime))
                if len(mementos) > 0:

                    redirect_location = response.get_headers("Location")

                    if redirect_location == mementos[-1].uri:
                        self.add_test_result(TestResult(name=TimeGateFutureRedirectTest.TIMEGATE_FUTURE_VALID_REDIRECT,
                                                        status=TestResult.TEST_PASS))
                    else:
                        self.add_test_result(
                            TestResult(name=TimeGateFutureRedirectTest.TIMEGATE_FUTURE_INVALID_REDIRECT,
                                       status=TestResult.TEST_WARN))

            except HeaderTypeNotFoundError:
                self.add_test_result(TestResult(name=TimeGateFutureRedirectTest.MISSING_REDIRECTION_LOCATION))

            except parser.ParserError:
                pass

        return self._test_report
