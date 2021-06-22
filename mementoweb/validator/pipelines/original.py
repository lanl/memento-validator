from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.content_negotiation_test import ContentNegotiationTest
from mementoweb.validator.tests.header_test import HeaderTest
from mementoweb.validator.tests.test import TestSetting, TestReport
from mementoweb.validator.tests.uri_test import URITest, URITestReport


class Original(DefaultPipeline):

    # TODO : Add original tests
    _tests: List[TestSetting] = [
        {'test': URITest(), 'params': None},
        {'test': URITest(), 'params': None}
    ]

    def validate(self, uri: str,
                 accept_datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:
        results = []

        URIResult: URITestReport = URITest().test(uri=uri)
        results.append(URIResult)

        HeaderResults = HeaderTest().test(URIResult.connection)
        results.append(HeaderResults)

        results.append(ContentNegotiationTest().test(URIResult.connection))

        return results