from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.content_type_header_test import ContentTypeHeaderTest
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.timemap_parse_test import TimeMapParseTest
from mementoweb.validator.tests.timemap_redirect_test import TimeMapRedirectTest
from mementoweb.validator.tests.uri_test import URITestReport, URITest


class TimeMap(DefaultPipeline):

    def validate(self, uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept='',
                 full: bool = False
                 ) -> List[TestReport]:
        results = []

        uri_result: URITestReport = URITest().test(uri=uri, datetime=datetime, method="GET")
        results.append(uri_result)

        if uri_result.report_status == TestReport.REPORT_FAIL:
            return results

        results.extend([
            TimeMapRedirectTest().test(connection=uri_result.connection),
            ContentTypeHeaderTest().test(response=uri_result.connection.get_response()),
            TimeMapParseTest().test(connection=uri_result.connection)
        ])

        # redirect_result = TimeMapRedirectTest().test(connection=uri_result.connection)
        # results.append(redirect_result)
        #
        # header_results = ContentTypeHeaderTest().test(uri_result.connection.get_response())
        # results.append(header_results)
        #
        # parse_results = TimeMapParseTest().test(uri_result.connection)
        # results.append(parse_results)

        if not full:
            return results

        # results.append(ContentNegotiationTest().test(uri_result.connection))

        return results
