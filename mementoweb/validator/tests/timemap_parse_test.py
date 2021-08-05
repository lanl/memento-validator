from mementoweb.validator.util.http import HttpConnection
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class TimeMapParseTest(BaseTest):
    TIMEMAP_PARSABLE = "TimeMap Parsable"

    TIMEMAP_NOT_PARSABLE = "TimeMap not parsable"

    def test(self, connection: HttpConnection) -> TestReport:

        try:
            parsed_body = connection.get_response().parse_body()
            self.add_test_result(TestResult(name=TimeMapParseTest.TIMEMAP_PARSABLE, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS
        except:
            self.add_test_result(TestResult(name=TimeMapParseTest.TIMEMAP_NOT_PARSABLE, status=TestResult.TEST_FAIL))

        return self._test_report
