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


class LinkHeaderTimeGateTestReport(TestReport):
    time_gate_uris: List[str] = []

    def __init__(self, time_gate_uris=None, *args, **kwargs):
        super(LinkHeaderTimeGateTestReport, self).__init__(*args, **kwargs)
        if time_gate_uris is None:
            time_gate_uris = []
        self.time_gate_uris = time_gate_uris

    def to_json(self):
        return_value = TestReport.to_json(self)
        return_value['timegates'] = self.time_gate_uris
        return return_value


class LinkHeaderTimeGateTest(LinkHeaderTest):

    _description = "Tests for the compliance of Link header timegate relation."

    TIMEGATE_PRESENT = "Timegate link present"

    TIMEGATE_NOT_PRESENT = "Timegate link present"

    _test_report: LinkHeaderTimeGateTestReport

    def __init__(self):
        super().__init__()
        self._test_report = LinkHeaderTimeGateTestReport(
            name=self._name(),
            description=self._description,
            report_status=TestReport.REPORT_FAIL,
            tests=[],
            time_gate_uris=[]
        )

    def test(self, response: HttpResponse, resource_type: ResourceType = ResourceType.ORIGINAL) -> \
            LinkHeaderTimeGateTestReport:
        # Just for typing support
        return typing.cast(LinkHeaderTimeGateTestReport,
                           super(LinkHeaderTimeGateTest, self).test(response, resource_type))

    def _test_original(self, response: HttpResponse) -> LinkHeaderTimeGateTestReport:
        self._test_report.report_status = TestReport.REPORT_PASS
        timegate_uris = response.search_link_headers("timegate")

        if not len(timegate_uris):
            self.add_test_result(TestResult(name=LinkHeaderTimeGateTest.TIMEGATE_NOT_PRESENT,
                                            status=TestResult.TEST_FAIL))
            self._test_report.report_status = TestReport.REPORT_FAIL
        else:
            self.add_test_result(TestResult(name=LinkHeaderTimeGateTest.TIMEGATE_PRESENT, status=TestResult.TEST_PASS))

            self._test_report.time_gate_uris = [timegate_uri.uri for timegate_uri in timegate_uris]

        return self._test_report

    def _test_memento(self, response: HttpResponse) -> LinkHeaderTimeGateTestReport:
        return self._test_original(response)
