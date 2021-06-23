from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.content_negotiation_test import ContentNegotiationTest
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.memento_redirect_test import MementoRedirectTest, MementoRedirectTestReport
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.uri_test import URITest, URITestReport


class Memento(DefaultPipeline):

    def validate(self, uri: str,
                 accept_datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:
        results = []

        # Check for the URI validity
        uri_report: URITestReport = URITest().test(uri=uri)
        results.append(uri_report)

        # If URI invalid  stop tests
        if uri_report.report_status is TestReport.REPORT_FAIL:
            return results

        # Check for any redirection
        memento_report: MementoRedirectTestReport = MementoRedirectTest().test(connection=uri_report.connection)
        results.append(memento_report)
        if memento_report.report_status is TestReport.REPORT_FAIL:
            return results

        # Check for content negotiation. i.e memento-datetime
        content_negotiation_report: TestReport = ContentNegotiationTest().test(uri_report.connection)
        results.append(content_negotiation_report)

        # Check for link headers and validate
        link_header_report = LinkHeaderTest().test(memento_report.connection, resource_type="memento")
        results.append(link_header_report)

        return results
