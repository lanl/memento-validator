from http.client import HTTPConnection
from typing import List

from mementoweb.validator import util
from mementoweb.validator.tests.test import BaseTest, TestResult, TEST_PASS, TEST_FAIL, TEST_WARN
from mementoweb.validator.util import parse_link_header, search_link_headers


class TimeGateTest(BaseTest):
    URI_ERROR: str = "URI ERROR"

    REDIRECTION_ANOTHER: str = "Redirection to another TimeGate"

    REDIRECTION_BEFORE: str = "Redirection before TimeGate"

    REDIRECTION_BEFORE_LOCATION = "Redirection before TimeGate does not have a location header"

    BROKEN_REDIRECTION = "Redirection to broken URI"

    def test(self, info: dict, params: dict = None) -> List[TestResult]:
        uri = info['uri']

        tests: List[TestResult] = []

        try:
            connection: HTTPConnection = util.http(uri)
        except Exception:
            return [self._test_result(uri, self.URI_ERROR)]

        # TODO: Add parse link
        response = connection.getresponse()
        status = response.status
        response_headers = dict(response.getheaders())
        vary = response_headers.get('vary', '')
        link_header_info = parse_link_header(response_headers['Link'])
        memento = search_link_headers(link_header_info, "rel=memento")[0]

        while 300 <= status <= 400 and not vary:

            # Get timegate original
            tg_original = search_link_headers(link_header_info, "rel=original")

            if tg_original:
                tests.append(self._test_result(uri, self.REDIRECTION_ANOTHER, test_status=TEST_PASS))
            else:
                tests.append(self._test_result(uri, self.REDIRECTION_BEFORE, test_status=TEST_WARN))

            uri = response_headers.get('location', '')

            if uri == '':
                tests.append(self._test_result(uri, self.REDIRECTION_BEFORE_LOCATION, test_status=TEST_FAIL))
                return tests

            try:
                connection = util.http(uri)
            except Exception:
                tests.append(self._test_result(uri, self.BROKEN_REDIRECTION, TEST_FAIL))
                return tests

            # TODO: Add parse link
            response = connection.getresponse()
            status = response.status
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

        return [self._test_result('uri', 'description')]
