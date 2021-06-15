from http.client import HTTPConnection
from typing import List

from mementoweb.validator import util
from mementoweb.validator.errors.uri_errors import HttpConnectionFailError, InvalidUriError, HttpRequestFailError
from mementoweb.validator.tests.test import BaseTest, TEST_PASS
from mementoweb.validator.tests.test import TestResult


class URITest(BaseTest):
    VALID_URI: str = "Valid URI"

    INVALID_URI: str = "Invalid URI"

    REQUEST_FAIL: str = "HTTP(s) Request Failed"

    CONNECTION_FAIL: str = "Could not connect to URI"

    def test(self, info: dict, params: dict = None) -> List[TestResult]:

        uri: str = info['uri']

        try:
            connection: HTTPConnection = util.http(uri)
        except InvalidUriError:
            return [self._test_result(uri, URITest.INVALID_URI)]
        except HttpConnectionFailError:
            return [self._test_result(uri, URITest.CONNECTION_FAIL)]
        except HttpRequestFailError:
            return [self._test_result(uri, URITest.REQUEST_FAIL)]

        return [self._test_result(uri, URITest.VALID_URI, test_status=TEST_PASS)]
