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
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.test import TestReport, TestResult


class LinkHeaderOriginalTest(LinkHeaderTest):

    _description = "Tests for the compliance of Link header original relation."

    ORIGINAL_NOT_PRESENT = "Original link not present"

    ORIGINAL_PRESENT = "Original link present"

    TIMEGATE_NOT_PRESENT = "Timegate link not present"

    TIMEGATE_PRESENT = "Timegate link present"

    def _test_memento(self, response: HttpResponse) -> TestReport:
        #  Original mandatory for memento
        self._test_report.report_status = TestReport.REPORT_PASS

        if not len(response.search_link_headers("original")):
            self.add_test_result(
                TestResult(name=LinkHeaderOriginalTest.ORIGINAL_NOT_PRESENT, status=TestResult.TEST_FAIL))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderOriginalTest.ORIGINAL_PRESENT, status=TestResult.TEST_PASS))

        return self._test_report

    def _test_timegate(self, response: HttpResponse) -> TestReport:
        return self._test_memento(response)
