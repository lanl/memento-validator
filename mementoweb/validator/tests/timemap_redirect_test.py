from mementoweb.validator.http import HttpConnection
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class TimeMapRedirectTest(BaseTest):
    TIMEMAP_RETURN_200 = "TimeMap returns 200"

    TIMEMAP_RETURN_INVALID_STATUS = "TimeMap does not return 200"

    def test(self, connection: HttpConnection) -> TestReport:
        response_status = connection.get_response().status

        if response_status == 200:
            self.add_test_result(TestResult(name=TimeMapRedirectTest.TIMEMAP_RETURN_200, status=TestResult.TEST_PASS))
            self._test_report.report_status = TestReport.REPORT_PASS

        else:
            self.add_test_result(TestResult(name=TimeMapRedirectTest.TIMEMAP_RETURN_INVALID_STATUS,
                                            status=TestResult.TEST_FAIL))

        return self._test_report
