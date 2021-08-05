from mementoweb.validator.util.http import http
from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.pipelines.default import PipelineResult
from mementoweb.validator.tests.header_test import HeaderTest
from mementoweb.validator.tests.link_header_memento_test import LinkHeaderMementoTest
from mementoweb.validator.tests.link_header_original_test import LinkHeaderOriginalTest
from mementoweb.validator.tests.link_header_timemap_test import LinkHeaderTimeMapTest
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.timegate_redirect_test import TimeGateRedirectTest
from mementoweb.validator.tests.uri_test import URITest
from mementoweb.validator.types import ResourceType


class TimeGate(DefaultPipeline):

    def __init__(self):

        super().__init__()

    def validate(self, uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept='',
                 past_datetime="Mon, 03 Feb 1992 00:00:00 GMT",
                 future_datetime="Tue, 03 Feb 2032 00:00:00 GMT",
                 ) -> PipelineResult:
        """
        Tests the memento implementation of a timegate resource.
        Steps

        1. Check the validity of the URI by compliance with the format and the establishing a connection.

        2. Check redirection and response status for the request. Redirected while the status is 3xx and not vary.

        3. Test the header of the response for "Location", "Content Location", "Vary", "Accept Datetime".

        4. Test content in link headers.

        5. Test redirection for different datetime combinations.

        :param uri: URI of the timegate for testing.
        :param datetime: Datetime for testing the timegate. Timegate is queries using the datetime provided.
        :param accept:
        :param past_datetime: Past datetime to test redirection of the timegate. Defaults to "Mon, 03 Feb 1992 00:00:00 GMT"
        :param future_datetime: Future datetime to test redirection of the timegate. Defaults to "Tue, 03 Feb 2032 00:00:00 GMT"
        :return:

        """
        self.result.reports = []
        uri_report = URITest().test(uri=uri, datetime=datetime)

        self.result.reports.append(uri_report)

        if uri_report.report_status is TestReport.REPORT_FAIL:
            return self.result

        redirect_report = TimeGateRedirectTest().test(connection=uri_report.connection, datetime=datetime)
        self.result.reports.append(redirect_report)

        if redirect_report.report_status is TestReport.REPORT_FAIL:
            return self.result

        header_report = HeaderTest().test(response=redirect_report.connection.get_response(),
                                          resource_type=ResourceType.TIMEGATE)
        lh_orig_report = LinkHeaderOriginalTest().test(response=redirect_report.connection.get_response(),
                                                       resource_type=ResourceType.TIMEGATE)
        lh_tm_report = LinkHeaderTimeMapTest().test(response=redirect_report.connection.get_response(),
                                                    resource_type=ResourceType.TIMEGATE)
        lh_mem_report = LinkHeaderMementoTest().test(response=redirect_report.connection.get_response(),
                                                     resource_type=ResourceType.TIMEGATE)
        blank_redirection_report = TimeGateRedirectTest().test(connection=redirect_report.connection,
                                                               test_type="blank",
                                                               datetime="",
                                                               assert_connection=http(uri, datetime=""))

        past_redirect_report = TimeGateRedirectTest().test(connection=redirect_report.connection,
                                                           test_type="past",
                                                           datetime=past_datetime,
                                                           assert_connection=http(uri, past_datetime))

        future_redirect_report = TimeGateRedirectTest().test(connection=redirect_report.connection,
                                                             test_type="future",
                                                             datetime=future_datetime,
                                                             assert_connection=http(uri, datetime=future_datetime))

        broken_redirect_report = TimeGateRedirectTest().test(connection=redirect_report.connection,
                                                             test_type="broken",
                                                             assert_connection=http(uri, datetime="BROKEN_DATETIME"),
                                                             datetime="BROKEN_DATETIME")
        self.result.reports.extend([
            header_report, lh_orig_report, lh_tm_report, lh_mem_report,
            blank_redirection_report, past_redirect_report, future_redirect_report, broken_redirect_report
        ])

        # Add extracted information to the result
        self.result.mementos = lh_mem_report.memento_uris
        self.result.timemaps = lh_tm_report.time_map_uris

        return self.result
