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

        uri_result: URITestReport = URITest().test(uri=uri)
        results.append(uri_result)

        header_results = ContentTypeHeaderTest().test(uri_result.connection.get_response())
        results.append(header_results)

        # results.append(ContentNegotiationTest().test(uri_result.connection))

        return results
