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
from mementoweb.validator.tests.content_type_header_test import ContentTypeHeaderTest
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.timemap_parse_test import TimeMapParseTest
from mementoweb.validator.tests.timemap_redirect_test import TimeMapRedirectTest
from mementoweb.validator.tests.uri_test import URITestReport, URITest


class TimeMap(DefaultPipeline):

    def __init__(self):

        super().__init__()

    def validate(self, uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept='',
                 full: bool = False
                 ) -> PipelineResult:
        self.result.reports = []

        uri_result: URITestReport = URITest().test(uri=uri, datetime=datetime, method="GET")
        self.result.reports.append(uri_result)

        if uri_result.report_status == TestReport.REPORT_FAIL:
            return self.result

        self.result.reports.extend([
            TimeMapRedirectTest().test(response=uri_result.connection.get_response()),
            ContentTypeHeaderTest().test(response=uri_result.connection.get_response()),
            TimeMapParseTest().test(response=uri_result.connection.get_response(), full_test=full)
        ])

        return self.result
