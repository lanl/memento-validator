from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.content_negotiation_test import ContentNegotiationTest
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.link_header_timegate_test import LinkHeaderTimeGateTest
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.uri_test import URITest, URITestReport


class Original(DefaultPipeline):
    # TODO : Add original tests

    def validate(self, uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:
        results = []

        uri_result: URITestReport = URITest().test(uri=uri, datetime=datetime)
        results.append(uri_result)

        # TODO: replace link header test with individual tests
        header_results = LinkHeaderTest().test(uri_result.connection.get_response())
        results.append(header_results)
        results.append(LinkHeaderTimeGateTest().test(uri_result.connection.get_response()))

        results.append(ContentNegotiationTest().test(uri_result.connection.get_response()))

        return results
