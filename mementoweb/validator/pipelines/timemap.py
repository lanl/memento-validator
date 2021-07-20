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
            TimeMapRedirectTest().test(connection=uri_result.connection),
            ContentTypeHeaderTest().test(response=uri_result.connection.get_response()),
            TimeMapParseTest().test(connection=uri_result.connection)
        ])

        # redirect_result = TimeMapRedirectTest().test(connection=uri_result.connection)
        # self.result.reports.append(redirect_result)
        #
        # header_self.result.reports = ContentTypeHeaderTest().test(uri_result.connection.get_response())
        # self.result.reports.append(header_self.result.reports)
        #
        # parse_self.result.reports = TimeMapParseTest().test(uri_result.connection)
        # self.result.reports.append(parse_self.result.reports)

        if not full:
            return self.result

        # self.result.reports.append(ContentNegotiationTest().test(uri_result.connection))

        return self.result
