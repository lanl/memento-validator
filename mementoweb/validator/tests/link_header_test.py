from enum import Enum
from typing import Dict, Callable

from mementoweb.validator.errors.header_errors import LinkHeaderNotFoundError, HeadersNotFoundError
from mementoweb.validator.http import HttpResponse
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class ResourceType(Enum):
    ORIGINAL = "original"

    MEMENTO = "memento"

    TIMEMAP = "timemap"

    TIMEGATE = "timegate"


class LinkHeaderTest(BaseTest):
    LINK_HEADER_NOT_PRESENT = "Link Header not present"

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

        except LinkHeaderNotFoundError:
            self._test_report.report_status = TestReport.REPORT_FAIL
            self.add_test_result(TestResult(name=LinkHeaderTest.LINK_HEADER_NOT_PRESENT))

        except HeadersNotFoundError:
            self._test_report.report_status = TestReport.REPORT_FAIL
            self.add_test_result(TestResult(name=LinkHeaderTest.HEADERS_NOT_PRESENT))

        return self._test_report

    def _test_original(self, response: HttpResponse) -> TestReport:
        return self._test_report

    def _test_memento(self, response: HttpResponse) -> TestReport:
        return self._test_report

    def _test_timemap(self, response: HttpResponse) -> TestReport:
        return self._test_report

    def _test_timegate(self, response: HttpResponse) -> TestReport:
        return self._test_report
