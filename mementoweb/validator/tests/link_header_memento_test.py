from dateutil import parser

from mementoweb.validator.http import HttpResponse
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.test import TestReport, TestResult


class LinkHeaderMementoTest(LinkHeaderTest):
    MEMENTO_NOT_PRESENT = "Memento link not present"

    MEMENTO_PRESENT = "Memento link present"

    SELECTED_MEMENTO_IN_LINK = "Selected memento in link header"

    SELECTED_MEMENTO_NOT_IN_LINK = "Selected memento not in link header"

    MEMENTO_DATETIME_PRESENT = "Memento contains datetime attribute"

    MEMENTO_DATETIME_NOT_PRESENT = "Memento does not contain datetime attribute"

    MEMENTO_DATETIME_PARSABLE = "Memento datetime parsable"

    MEMENTO_DATETIME_NOT_PARSABLE = "Memento datetime not parsable"

    def _test_timegate(self, response: HttpResponse) -> TestReport:
        # Same tests as for memento
        return self._test_memento(response)

    def _test_memento(self, response: HttpResponse) -> TestReport:

        memento_uri = response.uri
        mementos = response.search_link_headers("memento")

        if not len(mementos):
            self.add_test_result(
                TestResult(name=LinkHeaderMementoTest.MEMENTO_NOT_PRESENT, status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=LinkHeaderMementoTest.MEMENTO_PRESENT, status=TestResult.TEST_PASS))
            memento_uris = list(map(lambda x: x['link'], mementos))

            if memento_uri in memento_uris:
                self.add_test_result(TestResult(name=LinkHeaderMementoTest.SELECTED_MEMENTO_IN_LINK,
                                                status=TestResult.TEST_PASS))

            else:
                self.add_test_result(TestResult(LinkHeaderMementoTest.SELECTED_MEMENTO_NOT_IN_LINK,
                                                status=TestResult.TEST_WARN))

            for memento in mementos:
                if memento["datetime"]:
                    self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_PRESENT,
                                                    status=TestResult.TEST_PASS))
                    try:
                        parser.parse(memento["datetime"])
                        self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_PARSABLE,
                                                        status=TestResult.TEST_PASS))
                    except:
                        self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_NOT_PARSABLE,
                                                        status=TestResult.TEST_FAIL))
                else:
                    self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_NOT_PRESENT,
                                                    status=TestResult.TEST_FAIL))

            self._test_report.report_status = TestReport.REPORT_PASS

        return self._test_report
