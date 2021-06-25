from typing import Dict, Callable

from mementoweb.validator.errors.header_errors import LinkHeaderNotFoundError, HeadersNotFoundError
from mementoweb.validator.http import HttpResponse
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


class LinkHeaderTest(BaseTest):
    LINK_HEADER_NOT_PRESENT = "Link Header not present"

    HEADERS_NOT_PRESENT = "Headers not present"

    TIMEGATE_NOT_PRESENT = "Timegate link not present"

    TIMEBUNDLE_NOT_PRESENT = "Timebundle link not present"

    TIMEMAP_NOT_PRESENT = "Timemap link not present"

    TIMEGATE_PRESENT = "Timegate link present"

    TIMEBUNDLE_PRESENT = "Timebundle link present"

    TIMEMAP_PRESENT = "Timemap link present"

    MEMENTO_NOT_PRESENT = "Memento link not present"

    MEMENTO_PRESENT = "Memento link present"

    _tests: Dict[str, Callable[[HttpResponse], TestReport]]

    def __init__(self):
        super().__init__()
        self._tests = {
            "original": self._test_original,
            "memento": self._test_memento,
            "timemap": self._test_timemap,
            "timegate": self._test_timegate
        }

    def test(self, response: HttpResponse, resource_type="original") -> TestReport:

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
