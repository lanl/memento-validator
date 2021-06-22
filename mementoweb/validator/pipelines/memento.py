from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.content_negotiation_test import ContentNegotiationTest
from mementoweb.validator.tests.link_header_test import LinkHeaderTest
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.uri_test import URITest, URITestReport


class Memento(DefaultPipeline):

    def validate(self, uri: str,
                 accept_datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:
        # TODO : Add additional memento tests

        results = []

        URIResult: URITestReport = URITest().test(uri=uri)
        results.append(URIResult)

        HeaderResults = LinkHeaderTest().test(URIResult.connection)
        results.append(HeaderResults)

        results.append(ContentNegotiationTest().test(URIResult.connection))

        return results
