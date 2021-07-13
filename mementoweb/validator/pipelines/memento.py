from typing import List

from mementoweb.validator.http import HttpConnection
from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.content_negotiation_test import ContentNegotiationTest
from mementoweb.validator.tests.link_header_memento_test import LinkHeaderMementoTest
from mementoweb.validator.tests.link_header_original_test import LinkHeaderOriginalTest
from mementoweb.validator.tests.link_header_test import LinkHeaderTest, ResourceType
from mementoweb.validator.tests.link_header_timegate_test import LinkHeaderTimeGateTest
from mementoweb.validator.tests.link_header_timemap_test import LinkHeaderTimeMapTest
from mementoweb.validator.tests.memento_redirect_test import MementoRedirectTest, MementoRedirectTestReport
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.uri_test import URITest, URITestReport


class Memento(DefaultPipeline):

    def validate(self, uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:
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

        results = []

        # Check for the URI validity
        uri_report: URITestReport = URITest().test(uri=uri, datetime=datetime)
        results.append(uri_report)

        # If URI invalid  stop tests
        if uri_report.report_status is TestReport.REPORT_FAIL:
            return results

        # Check for any redirection, use already established connection and response
        connection: HttpConnection = uri_report.connection
        redirection_report: MementoRedirectTestReport = MementoRedirectTest().test(response=connection.get_response())
        results.append(redirection_report)
        # if memento_report.report_status is TestReport.REPORT_FAIL:
        #     return results

        # Check for content negotiation. i.e memento-datetime
        content_negotiation_report: TestReport = ContentNegotiationTest().test(uri_report.connection.get_response())
        results.append(content_negotiation_report)

        # Check for link headers and validate, use the updated connection response if redirected
        connection = redirection_report.connection or connection
        # link_header_report = LinkHeaderTest().test(connection.get_response(), resource_type=ResourceType.MEMENTO)
        # results.append(link_header_report)

        # Link-header tests
        results.append(LinkHeaderOriginalTest().test(response=connection.get_response(),
                                                     resource_type=ResourceType.MEMENTO))

        results.append(LinkHeaderTimeGateTest().test(response=connection.get_response(),
                                                     resource_type=ResourceType.MEMENTO))

        results.append(LinkHeaderTimeMapTest().test(response=connection.get_response(),
                                                    resource_type=ResourceType.MEMENTO))

        results.append(LinkHeaderMementoTest().test(response=connection.get_response(),
                                                    resource_type=ResourceType.MEMENTO))

        return results
