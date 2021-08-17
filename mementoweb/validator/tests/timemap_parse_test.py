from dateutil import parser
from mementoweb.validator.util.http import HttpConnection
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class TimeMapParseTest(BaseTest):

    TIMEMAP_PARSABLE = "TimeMap Parsable"

    TIMEMAP_NOT_PARSABLE = "TimeMap not parsable"

    MEMENTO_DATETIME_PRESENT = "Memento contains datetime attribute"

    MEMENTO_DATETIME_NOT_PRESENT = "Memento does not contain datetime attribute"

    MEMENTO_DATETIME_PARSABLE = "Memento datetime parsable"

    MEMENTO_DATETIME_NOT_PARSABLE = "Memento datetime not parsable"

    def test(self, connection: HttpConnection, full_test=False) -> TestReport:

        try:
            parsed_body = connection.get_response().parse_body()
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
            # if full_test:
            #     for parsed

        except:
            self.add_test_result(TestResult(name=TimeMapParseTest.TIMEMAP_NOT_PARSABLE, status=TestResult.TEST_FAIL))

        return self._test_report
