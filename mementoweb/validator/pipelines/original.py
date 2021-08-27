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

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.pipelines.default import PipelineResult
from mementoweb.validator.tests.datetime_negotiation_test import DatetimeNegotiationTest
from mementoweb.validator.tests.link_header_timegate_test import LinkHeaderTimeGateTest
from mementoweb.validator.tests.link_header_timemap_test import LinkHeaderTimeMapTest
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.uri_test import URITest, URITestReport
from mementoweb.validator.validator_types import ResourceType


class Original(DefaultPipeline):

    def __init__(self):
        super().__init__()

    def validate(self, uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> PipelineResult:
        self.result.reports = []

        uri_report: URITestReport = URITest().test(uri=uri, datetime=datetime)
        self.result.reports.append(uri_report)

        if uri_report.report_status is TestReport.REPORT_FAIL:
            return self.result

        lh_tm_report = LinkHeaderTimeMapTest().test(response=uri_report.connection.get_response(),
                                                    resource_type=ResourceType.ORIGINAL)
        lh_tg_report = LinkHeaderTimeGateTest().test(response=uri_report.connection.get_response(),
                                                     resource_type=ResourceType.ORIGINAL)

        content_negotiation_report = DatetimeNegotiationTest().test(response=uri_report.connection.get_response())

        self.result.reports.extend([
            content_negotiation_report,
            lh_tm_report,
            lh_tg_report
        ])

        self.result.timemaps = lh_tm_report.time_map_uris
        self.result.timegates = lh_tg_report.time_gate_uris

        return self.result
