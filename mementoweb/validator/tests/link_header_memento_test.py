import re
import typing
from typing import List

from dateutil import parser

from mementoweb.validator.util.http import HttpResponse, http
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.test import TestReport, TestResult
from mementoweb.validator.validator_types import ResourceType


class LinkHeaderMementoTestReport(TestReport):
    memento_uris: List[str] = []

    def __init__(self, memento_uris=None, *args, **kwargs):
        super(LinkHeaderMementoTestReport, self).__init__(*args, **kwargs)
        if memento_uris is None:
            memento_uris = []
        self.memento_uris = memento_uris


class LinkHeaderMementoTest(LinkHeaderTest):
    MEMENTO_NOT_PRESENT = "Memento link not present"

    MEMENTO_PRESENT = "Memento link present"

    SELECTED_MEMENTO_IN_LINK = "Selected memento in link header"

    SELECTED_MEMENTO_NOT_IN_LINK = "Selected memento not in link header"

    MEMENTO_DATETIME_PRESENT = "Memento contains datetime attribute"

    MEMENTO_DATETIME_NOT_PRESENT = "Memento does not contain datetime attribute"

    MEMENTO_DATETIME_PARSABLE = "Memento datetime parsable"

    MEMENTO_DATETIME_NOT_PARSABLE = "Memento datetime not parsable"

    NO_TIMEMAP_LINK_FOR_TIMEMAP_TESTS = "No timemap link for timemap tests"

    FIRST_MEMENTO_MATCHES_TIMEMAP_FIRST = "First Memento matches first in the Timemap"

    FIRST_MEMENTO_DOES_NOT_MATCH_TIMEMAP_FIRST = "First Memento does not match first in the Timemap"

    LAST_MEMENTO_MATCHES_TIMEMAP_LAST = "Last Memento matches last in the Timemap"

    LAST_MEMENTO_DOES_NOT_MATCH_TIMEMAP_LAST = "Last Memento does not match last in the Timemap"

    _test_report: LinkHeaderMementoTestReport

    def __init__(self):
        super().__init__()
        self._test_report = LinkHeaderMementoTestReport(
            name=self._name(),
            description=self._description,
            report_status=TestReport.REPORT_FAIL,
            tests=[]
        )

    def test(self, response: HttpResponse, resource_type: ResourceType = ResourceType.ORIGINAL) -> \
            LinkHeaderMementoTestReport:
        # Just for typing support
        return typing.cast(LinkHeaderMementoTestReport,
                           super(LinkHeaderMementoTest, self).test(response, resource_type))

    def _test_timegate(self, response: HttpResponse) -> TestReport:
        # Same tests as for memento
        # TODO : Add modification here (move _test_memento and modification to _test_memento ?? )
        return self._test_memento(response)

    def _test_memento(self, response: HttpResponse) -> TestReport:

        memento_uri = response.uri
        self._mementos = response.search_link_headers("memento", regex=True)

        if not len(self._mementos):
            self.add_test_result(
                TestResult(name=LinkHeaderMementoTest.MEMENTO_NOT_PRESENT, status=TestResult.TEST_FAIL))
        else:
            self.add_test_result(TestResult(name=LinkHeaderMementoTest.MEMENTO_PRESENT, status=TestResult.TEST_PASS))
            memento_uris = list(map(lambda x: x.uri, self._mementos))
            self._test_report.memento_uris = memento_uris

            if memento_uri in memento_uris:
                self.add_test_result(TestResult(name=LinkHeaderMementoTest.SELECTED_MEMENTO_IN_LINK,
                                                status=TestResult.TEST_PASS))

            else:
                self.add_test_result(TestResult(LinkHeaderMementoTest.SELECTED_MEMENTO_NOT_IN_LINK,
                                                status=TestResult.TEST_WARN))

            for memento in self._mementos:
                if memento.datetime:
                    self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_PRESENT,
                                                    status=TestResult.TEST_PASS))
                    try:
                        parser.parse(memento.datetime)
                        self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_PARSABLE,
                                                        status=TestResult.TEST_PASS))

                        self._full_timemap_test(response)

                    except parser.ParserError:
                        self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_NOT_PARSABLE,
                                                        status=TestResult.TEST_FAIL))
                else:
                    self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_NOT_PRESENT,
                                                    status=TestResult.TEST_FAIL))

        return self._test_report

    def _full_timemap_test(self, response, resource_type="memento"):
        try:
            self._mementos.sort(key=lambda x: parser.parse(x.datetime))
            timemaps = response.search_link_headers("timemap")

            if not timemaps:
                self.add_test_result(TestResult(LinkHeaderMementoTest.NO_TIMEMAP_LINK_FOR_TIMEMAP_TESTS,
                                                status=TestResult.TEST_WARN))
            else:
                self._timemap_response = http(timemaps[0].uri, method="GET")
                timemap_body_links = self._timemap_response.get_response().parse_body()
                filtered_links = list(filter(lambda x: re.findall('self', x.relationship), timemap_body_links))

                partial_timemap = False

                for filtered_link in filtered_links:
                    if filtered_link.link_from and filtered_link.link_from != self._mementos[0].datetime:
                        partial_timemap = True
                    elif filtered_link.link_until and filtered_link.link_until != self._mementos[0].datetime:
                        partial_timemap = True

                timemap_memento_links = list(filter(lambda x: re.findall('memento', x.relationship), timemap_body_links))
                timemap_memento_links.sort(key=lambda x: parser.parse(x.datetime))

                if not partial_timemap:
                    if self._mementos[0].uri == timemap_memento_links[0].uri:
                        self.add_test_result(TestResult(LinkHeaderMementoTest.FIRST_MEMENTO_MATCHES_TIMEMAP_FIRST,
                                                        status=TestResult.TEST_PASS))
                    else:
                        self.add_test_result(TestResult(
                            LinkHeaderMementoTest.FIRST_MEMENTO_DOES_NOT_MATCH_TIMEMAP_FIRST,
                            status=TestResult.TEST_WARN))

                    if self._mementos[-1].uri == timemap_memento_links[-1].uri:
                        self.add_test_result(TestResult(LinkHeaderMementoTest.LAST_MEMENTO_MATCHES_TIMEMAP_LAST,
                                                        status=TestResult.TEST_PASS))
                    else:
                        self.add_test_result(TestResult(
                            LinkHeaderMementoTest.LAST_MEMENTO_DOES_NOT_MATCH_TIMEMAP_LAST,
                            status=TestResult.TEST_WARN))

                    # if resource_type=="memento":
        #              TODO : Complete with previous, next links

        except parser.ParserError:
            self.add_test_result(TestResult(LinkHeaderMementoTest.MEMENTO_DATETIME_NOT_PARSABLE,
                                            status=TestResult.TEST_FAIL))
