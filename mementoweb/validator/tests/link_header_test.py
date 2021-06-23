from typing import Dict, Callable

from mementoweb.validator.errors.header_errors import LinkHeaderNotFoundError, HeadersNotFoundError
from mementoweb.validator.http import HttpConnection
from mementoweb.validator.tests.test import BaseTest, TestReport, TestResult


# TODO : REFACTOR
class LinkHeaderTest(BaseTest):
    LINK_HEADER_NOT_PRESENT = "Link Header not present"

    HEADERS_NOT_PRESENT = "Headers not present"

    TIMEGATE_NOT_PRESENT = "Timegate link not present"

    TIMEBUNDLE_NOT_PRESENT = "Timebundle link not present"

    TIMEMAP_NOT_PRESENT = "Timemap link not present"

    TIMEGATE_PRESENT = "Timegate link present"

    TIMEBUNDLE_PRESENT = "Timebundle link present"

    TIMEMAP_PRESENT = "Timemap link present"

    ORIGINAL_NOT_PRESENT = "Original link not present"

    ORIGINAL_PRESENT = "Original link present"

    MEMENTO_NOT_PRESENT = "Memento link not present"

    MEMENTO_PRESENT = "Memento link present"

    TIMEMAP_TYPE_PRESENT = "Timemap type present"

    TIMEMAP_TYPE_NOT_PRESENT = "Timemap type not present"

    _tests: Dict[str, Callable[[HttpConnection], TestReport]]

    def __init__(self):
        super().__init__()
        self._tests = {
            "original": self._test_original,
            "memento": self._test_memento
        }

    def test(self, connection: HttpConnection, resource_type="original") -> TestReport:

        try:
            return self._tests[resource_type](connection)

        except LinkHeaderNotFoundError:
            self._test_report.report_status = TestReport.REPORT_FAIL
            self.add_test_result(TestResult(name=LinkHeaderTest.LINK_HEADER_NOT_PRESENT))

        except HeadersNotFoundError:
            self._test_report.report_status = TestReport.REPORT_FAIL
            self.add_test_result(TestResult(name=LinkHeaderTest.HEADERS_NOT_PRESENT))

        return self._test_report

    def _test_original(self, connection: HttpConnection) -> TestReport:
        # TODO : Double check tests with std
        self._test_report.report_status = TestReport.REPORT_PASS

        if not len(connection.search_link_headers("timegate")):
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEGATE_NOT_PRESENT))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEGATE_PRESENT, status=TestResult.TEST_PASS))

        if not len(connection.search_link_headers("timebundle")):
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEBUNDLE_NOT_PRESENT))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEBUNDLE_PRESENT, status=TestResult.TEST_PASS))

        if not len(connection.search_link_headers("timemap")):
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEMAP_NOT_PRESENT))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))

        return self._test_report

    def _test_memento(self, connection: HttpConnection):
        # TODO: Add memento tests
        self._test_report.report_status = TestReport.REPORT_PASS
        if not len(connection.search_link_headers("original")):
            self.add_test_result(TestResult(name=LinkHeaderTest.ORIGINAL_NOT_PRESENT))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTest.ORIGINAL_PRESENT, status=TestResult.TEST_PASS))

        if not len(connection.search_link_headers("timegate")):
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEGATE_NOT_PRESENT))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEGATE_PRESENT, status=TestResult.TEST_PASS))

        timemaps = connection.search_link_headers("timemap")
        if not len(timemaps):
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEMAP_NOT_PRESENT, status=TestResult.TEST_WARN))
            self._test_report.report_status = TestReport.REPORT_WARN
        else:
            self.add_test_result(TestResult(name=LinkHeaderTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))
            timemap: dict
            for timemap in timemaps:
                # TODO : add matching content type
                if "type" in timemap.keys() and timemap["type"] == "application/link-format":
                    self.add_test_result(TestResult(LinkHeaderTest.TIMEMAP_TYPE_PRESENT, status=TestResult.TEST_PASS))
                else:
                    self.add_test_result(TestResult(LinkHeaderTest.TIMEMAP_TYPE_NOT_PRESENT))

        mementos = connection.search_link_headers("memento")

        if not len(mementos):
            self.add_test_result(TestResult(LinkHeaderTest.MEMENTO_NOT_PRESENT, status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(LinkHeaderTest.MEMENTO_NOT_PRESENT, status=TestResult.TEST_PASS))

        return self._test_report
