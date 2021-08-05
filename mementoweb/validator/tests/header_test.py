from typing import Dict, Callable

from mementoweb.validator.errors.header_errors import HeadersNotFoundError
from mementoweb.validator.util.http import HttpResponse
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult
from mementoweb.validator.types import ResourceType


class HeaderTest(BaseTest):
    HEADERS_NOT_PRESENT = "Headers not present"

    _tests: Dict[ResourceType, Callable[[HttpResponse], TestReport]]

    def __init__(self):
        super().__init__()
        self._tests = {
            ResourceType.ORIGINAL: self._test_original,
            ResourceType.MEMENTO: self._test_memento,
            ResourceType.TIMEMAP: self._test_timemap,
            ResourceType.TIMEGATE: self._test_timegate
        }

    def test(self, response: HttpResponse, resource_type: ResourceType = ResourceType.ORIGINAL) -> TestReport:

        try:
            return self._tests[resource_type](response)

        except HeadersNotFoundError:
            self._test_report.report_status = TestReport.REPORT_FAIL
            self.add_test_result(TestResult(name=HeaderTest.HEADERS_NOT_PRESENT))

        return self._test_report

    def _test_original(self, response: HttpResponse) -> TestReport:
        return self._test_report

    def _test_memento(self, response: HttpResponse) -> TestReport:
        return self._test_report

    def _test_timemap(self, response: HttpResponse) -> TestReport:
        return self._test_report

    def _test_timegate(self, response: HttpResponse) -> TestReport:
        # TODO: refactor error names to variables
        self._test_report.report_status = TestReport.REPORT_PASS

        if "Location" in response.header_keys():
            self.add_test_result(TestResult(name="Location Header found", status=TestResult.TEST_PASS))

        elif "Content-Location" in response.header_keys():
            self.add_test_result(TestResult(name="Content Location Header found", status=TestResult.TEST_PASS))

        else:
            self.add_test_result(TestResult(name="Location/ Content-Location header not found",
                                            status=TestResult.TEST_FAIL))
            self._test_report.report_status = TestReport.REPORT_FAIL

        if "Vary" not in response.header_keys():
            self.add_test_result(TestResult(name="Vary header not found", status=TestResult.TEST_FAIL))

        else:
            if "accept-datetime" in response.get_headers("Vary").lower():
                self.add_test_result(TestResult(name="Accept-Datetime in vary header", status=TestResult.TEST_PASS))
            else:
                self.add_test_result(TestResult(name="Accept-Datetime not in vary header", status=TestResult.TEST_FAIL))

        return self._test_report
