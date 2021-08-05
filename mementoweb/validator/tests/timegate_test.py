from typing import List

from mementoweb.validator import util
from mementoweb.validator.util.http import HttpConnection, http
from mementoweb.validator.tests.test import BaseTest, TestReport


class TimeGateTest(BaseTest):
    URI_ERROR: str = "URI ERROR"

    REDIRECTION_ANOTHER: str = "Redirection to another TimeGate"

    REDIRECTION_BEFORE: str = "Redirection before TimeGate"

    REDIRECTION_BEFORE_LOCATION = "Redirection before TimeGate does not have a location header"

    BROKEN_REDIRECTION = "Redirection to broken URI"

    def test(self, uri: str = None) -> List[TestReport]:

        tests: List[TestReport] = []

        try:
            connection: HttpConnection = http.http(uri)
        except Exception:
            return [self._test_report(uri, self.URI_ERROR)]

        # TODO: Add parse link
        response = connection.get_response()
        status = response.report_status
        response_headers = dict(response.getheaders())
        vary = response_headers.get('vary', '')
        link_header_info = dict()
        if 'Link' in response_headers.keys():
            link_header_info = parse_link_header(response_headers['Link'])
            # Memento not required
            # memento = search_link_headers(link_header_info, "rel=memento")[0]

        while 300 <= status <= 400 and not vary:

            # Get timegate original
            tg_original = search_link_headers(link_header_info, "rel=original")

            if tg_original:
                tests.append(self._test_report(uri, self.REDIRECTION_ANOTHER, report_status=TEST_PASS))
            else:
                tests.append(self._test_report(uri, self.REDIRECTION_BEFORE, report_status=TEST_WARN))

            uri = response_headers.get('location', '')

            if uri == '':
                tests.append(self._test_report(uri, self.REDIRECTION_BEFORE_LOCATION, report_status=TEST_FAIL))
                return tests

            try:
                connection = util.http(uri)
            except Exception:
                tests.append(self._test_report(uri, self.BROKEN_REDIRECTION, TEST_FAIL))
                return tests

            # TODO: Add parse link
            response = connection.getresponse()
            status = response.report_status
            response_headers = dict(response.getheaders())
            vary = response_headers.get('vary', '')

        # resp = connection.getresponse()
        # status = resp.status
        # out_headers = dict(resp.getheaders())
        # body = resp.read()
        # connection.close()
        # # get headers
        # vary = out_headers.get('vary', '')

        # parse links and get information, parse memento information
        # link = out_headers.get('link', {})
        # mem = ''

        return [self._test_report('uri', 'description')]
