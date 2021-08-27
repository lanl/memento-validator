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

from mementoweb.validator.util.http import HttpResponse
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class TimeMapRedirectTest(BaseTest):
    """

        Implements testing procedures/ variables for testing redirection of a timemap resource.

    """

    TIMEMAP_VALID_RETURN = "TimeMap returns 200"

    TIMEMAP_INVALID_RETURN = "TimeMap does not return 200"

    def test(self, response: HttpResponse) -> TestReport:
        """

            Performs timemap redirection tests for a given HTTP response.

        :param response: HTTP response for testing
        :return: Base test report containing test results.
        """
        response_status = response.status

        if response_status == 200:
            self.add_test_result(TestResult(name=TimeMapRedirectTest.TIMEMAP_VALID_RETURN, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS

        else:
            self.add_test_result(TestResult(name=TimeMapRedirectTest.TIMEMAP_INVALID_RETURN,
                                            status=TestResult.TEST_FAIL))

        return self._test_report
