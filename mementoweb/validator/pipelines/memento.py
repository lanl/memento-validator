from mementoweb.validator.util.http import HttpConnection
from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.pipelines.default import PipelineResult
from mementoweb.validator.tests.datetime_negotiation_test import DatetimeNegotiationTest
from mementoweb.validator.tests.link_header_memento_test import LinkHeaderMementoTest
from mementoweb.validator.tests.link_header_original_test import LinkHeaderOriginalTest
from mementoweb.validator.tests.link_header_test import ResourceType
from mementoweb.validator.tests.link_header_timegate_test import LinkHeaderTimeGateTest
from mementoweb.validator.tests.link_header_timemap_test import LinkHeaderTimeMapTest
from mementoweb.validator.tests.memento_redirect_test import MementoRedirectTest, MementoRedirectTestReport
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.uri_test import URITest, URITestReport


class Memento(DefaultPipeline):

    def __init__(self):

        super().__init__()

    def validate(self, uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> PipelineResult:
        """
        Test sequence for Memento resource type.
        Steps

        1. Check the validity of the URI
            Checks the URI compliance with standard format and by establishing connection

        2. Check redirection
            Check the response status of connection by performing redirection (status 3xx)

        3. Check content negotiation
            Check for memento datetime header

        4. Link header tests

        :param uri: URI of the memento
        :param datetime:
        :param accept:
        :return: Test reports
        """

        self.result.reports = []

        self.result.reports = []

        # Check for the URI validity
        uri_report: URITestReport = URITest().test(uri=uri, datetime=datetime)
        self.result.reports.append(uri_report)

        # If URI invalid  stop tests
        if uri_report.report_status is TestReport.REPORT_FAIL:
            return self.result

        # Check for any redirection, use already established connection and response
        connection: HttpConnection = uri_report.connection
        redirection_report: MementoRedirectTestReport = MementoRedirectTest().test(response=connection.get_response())
        self.result.reports.append(redirection_report)
        if redirection_report.report_status is TestReport.REPORT_FAIL:
            return self.result

        connection = redirection_report.connection or connection

        # Check for content negotiation. i.e memento-datetime
        content_negotiation_report: TestReport = DatetimeNegotiationTest().test(uri_report.connection.get_response())
        self.result.reports.append(content_negotiation_report)

        # Check for link headers and validate, use the updated connection response if redirected
        # link_header_report = LinkHeaderTest().test(connection.get_response(), resource_type=ResourceType.MEMENTO)
        # self.result.reports.append(link_header_report)

        # Link-header tests
        self.result.reports.append(LinkHeaderOriginalTest().test(response=connection.get_response(),
                                                                 resource_type=ResourceType.MEMENTO))

        self.result.reports.append(LinkHeaderMementoTest().test(response=connection.get_response(),
                                                                resource_type=ResourceType.MEMENTO))
        lh_tm_report = LinkHeaderTimeMapTest().test(response=connection.get_response(), resource_type=ResourceType.MEMENTO)

        lh_tg_report = LinkHeaderTimeGateTest().test(response=connection.get_response(), resource_type=ResourceType.MEMENTO)
        self.result.reports.extend([
            lh_tm_report, lh_tg_report
        ])

        self.result.timemaps = lh_tm_report.time_map_uris
        self.result.timegates = lh_tg_report.time_gate_uris

        return self.result
