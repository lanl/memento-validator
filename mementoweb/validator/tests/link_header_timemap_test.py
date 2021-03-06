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

import typing
from typing import List

from mementoweb.validator.util.http import HttpResponse
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.test import TestReport, TestResult
from mementoweb.validator.validator_types import ResourceType


class LinkHeaderTimeMapTestReport(TestReport):
    """
        Test report from Link header timemap relation test.
        Includes extracted timemap uris in addition to standard test report.
    """
    time_map_uris: List[str] = []

    def __init__(self, time_map_uris=None, *args, **kwargs):
        super(LinkHeaderTimeMapTestReport, self).__init__(*args, **kwargs)
        if time_map_uris is None:
            time_map_uris = []
        self.time_map_uris = time_map_uris

    def to_json(self):
        return_value = TestReport.to_json(self)
        return_value['timemaps'] = self.time_map_uris
        return return_value


class LinkHeaderTimeMapTest(LinkHeaderTest):
    """

        Implements testing procedures, variables for link header timemap relation.

    """

    _description = "Tests the compliance of Link header timemap relation."

    TIMEMAP_PRESENT = "Timemap link present"

    TIMEMAP_NOT_PRESENT = "Timemap link not present"

    TIMEMAP_TYPE_PRESENT = "Timemap type present"

    TIMEMAP_TYPE_NOT_PRESENT = "Timemap type not present"

    _test_report: LinkHeaderTimeMapTestReport

    def __init__(self):
        super().__init__()
        self._test_report = LinkHeaderTimeMapTestReport(
            name=self._name(),
            description=self._description,
            report_status=TestReport.REPORT_FAIL,
            tests=[],
            time_map_uris=[]
        )

    def test(self, response: HttpResponse, resource_type: ResourceType = ResourceType.ORIGINAL) -> \
            LinkHeaderTimeMapTestReport:
        """

        Performs tests on Link header timemap relation for a given HTTP response.

        :param response: HTTP response for testing
        :param resource_type: type of resource.
        :return: Link header timemap test report.
        """
        # Just for typing support
        return typing.cast(LinkHeaderTimeMapTestReport,
                           super(LinkHeaderTimeMapTest, self).test(response, resource_type))

    def _test_timegate(self, response: HttpResponse) -> LinkHeaderTimeMapTestReport:
        self._test_report.report_status = TestReport.REPORT_PASS
        timemaps = response.search_link_headers('timemap')
        if not timemaps:
            self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_NOT_PRESENT,
                                            status=TestResult.TEST_WARN))
        else:
            self.add_test_result(TestResult(LinkHeaderTimeMapTest.TIMEMAP_PRESENT, status=TestResult.TEST_PASS))

            for timemap in timemaps:
                if timemap.link_type == "application/link-format":
                    self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_TYPE_PRESENT,
                                                    status=TestResult.TEST_PASS))
                    self._test_report.time_map_uris.append(timemap.uri)

            if not self._test_report.time_map_uris:
                # We dont have any valid time map uris -> Fail the report
                self.add_test_result(TestResult(name=LinkHeaderTimeMapTest.TIMEMAP_TYPE_NOT_PRESENT,
                                                status=TestResult.TEST_FAIL))
                self._test_report.report_status = TestReport.REPORT_FAIL

        return self._test_report

    def _test_memento(self, response: HttpResponse) -> LinkHeaderTimeMapTestReport:
        return self._test_timegate(response)

    def _test_original(self, response: HttpResponse) -> LinkHeaderTimeMapTestReport:
        return self._test_timegate(response)
