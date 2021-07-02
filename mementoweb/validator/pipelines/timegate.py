from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.header_test import HeaderTest
from mementoweb.validator.tests.link_header_memento_test import LinkHeaderMementoTest
from mementoweb.validator.tests.link_header_timemap_test import LinkHeaderTimeMapTest
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.timegate_redirect_test import TimeGateRedirectTest
from mementoweb.validator.tests.uri_test import URITest
from mementoweb.validator.types import ResourceType


class TimeGate(DefaultPipeline):

    def validate(self, uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:
        results: [TestReport] = []
        uri_report = URITest().test(uri=uri, datetime=datetime)

        results.append(uri_report)

        if uri_report.report_status is TestReport.REPORT_FAIL:
            return results

        redirect_report = TimeGateRedirectTest().test(connection=uri_report.connection, datetime=datetime)
        results.append(redirect_report)

        if redirect_report.report_status is TestReport.REPORT_FAIL:
            return results

        results.extend([
            HeaderTest().test(response=redirect_report.connection.get_response(), resource_type=ResourceType.TIMEGATE),
            LinkHeaderTimeMapTest().test(response=redirect_report.connection.get_response(),
                                         resource_type=ResourceType.TIMEGATE),
            LinkHeaderMementoTest().test(response=redirect_report.connection.get_response(),
                                         resource_type=ResourceType.TIMEGATE)
        ])

        # Do link_header tests

        return results
