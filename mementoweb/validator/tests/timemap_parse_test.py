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
from mementoweb.validator.util.http import HttpResponse
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class TimeMapParseTest(BaseTest):
    """

        Implements testing procedures/ variables for testing Timemap resource body.

    """
    TIMEMAP_PARSABLE = "TimeMap Parsable"

    TIMEMAP_NOT_PARSABLE = "TimeMap not parsable"

    MEMENTO_DATETIME_PRESENT = "Memento contains datetime attribute"

    MEMENTO_DATETIME_NOT_PRESENT = "Memento does not contain datetime attribute"

    MEMENTO_DATETIME_PARSABLE = "Memento datetime parsable"

    MEMENTO_DATETIME_NOT_PARSABLE = "Memento datetime not parsable"

    def test(self, response: HttpResponse, full_test=False) -> TestReport:
        """

        Tests the parsability/ validity of timemap resource body of a given Http response.

        :param response: Http response for testing
        :param full_test: Toogle full tests. Individually test each
        memento and test the parsability of corresponding datetime.
        :return: Base test report containing test results.
        """

        try:
            parsed_body = response.parse_body()
            self.add_test_result(TestResult(name=TimeMapParseTest.TIMEMAP_PARSABLE, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS
            if full_test:
                mementos = list(filter(lambda x: x.relationship == "memento", parsed_body))
                for memento in mementos:
                    if memento.datetime:
                        self.add_test_result(TestResult(TimeMapParseTest.MEMENTO_DATETIME_PRESENT,
                                                        status=TestResult.TEST_PASS))
                        try:
                            parser.parse(memento.datetime)
                            self.add_test_result(TestResult(TimeMapParseTest.MEMENTO_DATETIME_PARSABLE,
                                                            status=TestResult.TEST_PASS))

                        except parser.ParserError:
                            self.add_test_result(TestResult(TimeMapParseTest.MEMENTO_DATETIME_NOT_PARSABLE,
                                                            status=TestResult.TEST_FAIL))
                    else:
                        self.add_test_result(TestResult(TimeMapParseTest.MEMENTO_DATETIME_NOT_PRESENT,
                                                        status=TestResult.TEST_FAIL))

        except:
            self.add_test_result(TestResult(name=TimeMapParseTest.TIMEMAP_NOT_PARSABLE, status=TestResult.TEST_FAIL))

        return self._test_report
