from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.content_type_header_test import ContentTypeHeaderTest
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.uri_test import URITestReport, URITest


class TimeMap(DefaultPipeline):

    def validate(self, uri: str,
                 accept_datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:
        results = []

        URIResult: URITestReport = URITest().test(uri=uri)
        results.append(URIResult)

        HeaderResults = ContentTypeHeaderTest().test(URIResult.connection)
        results.append(HeaderResults)

        # results.append(ContentNegotiationTest().test(URIResult.connection))

        return results
