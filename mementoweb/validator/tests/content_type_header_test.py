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

from mementoweb.validator.errors.header_errors import HeaderTypeNotFoundError
from mementoweb.validator.util.http import HttpResponse
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult

"""
    Tests for compliance with expected content-type header in the response.
"""


class ContentTypeHeaderTest(BaseTest):
    CONTENT_TYPE_NOT_PRESENT = "Content-type not present for Time-map"

    CONTENT_TYPE_PRESENT = "Content-type present for Time-map"

    CONTENT_TYPE_MATCH = "Content type match"

    CONTENT_TYPE_MISMATCH = "Content type mismatch"

    def test(self, response: HttpResponse, content_type: str = None) -> TestReport:

        try:
            self._test_report.report_status = TestReport.REPORT_PASS

            response_content_type = response.get_headers("Content-Type")

            if content_type:
                if content_type in response_content_type:
                    self.add_test_result(
                        TestResult(name=ContentTypeHeaderTest.CONTENT_TYPE_MATCH, status=TestResult.TEST_PASS))
                else:
                    self.add_test_result(
                        TestResult(name=ContentTypeHeaderTest.CONTENT_TYPE_MISMATCH, status=TestResult.TEST_WARN))
            else:
                self.add_test_result(
                    TestResult(ContentTypeHeaderTest.CONTENT_TYPE_PRESENT, status=TestResult.TEST_PASS))

        except HeaderTypeNotFoundError:
            self._test_report.report_status = TestReport.REPORT_FAIL
            self.add_test_result(TestResult(name=ContentTypeHeaderTest.CONTENT_TYPE_NOT_PRESENT))

        return self._test_report
