from urllib.parse import urlparse, ParseResult
from http.client import HTTPConnection, HTTPSConnection
from mementoweb.validator.tests.test import TestResult
from mementoweb.validator.tests.test import BaseTest


class URITest(BaseTest):

    VALID_URI: str = "Valid URI"

    INVALID_URI: str = "Invalid URI"

    REQUEST_FAIL: str = "HTTP(s) Request Failed"

    def test(self, info: dict, params: dict = {}) -> TestResult:

        uri: str = info['uri']

        params: ParseResult = urlparse(url=uri)

        # TODO - Check tuple handling validatorhandler 212 (Python 2.4 fix??)
        host: str = params.netloc
        if params.port == 80:
            # required??
            host = params.netloc.replace(':80', '')

        if not host:
            return self._test_result(uri, URITest.INVALID_URI)

        path = params.path

        if path and path[0] != '/':
            path = '/' + path

        if not params.query:
            path = path + "?" + params.query

        try:
            if params.scheme == 'http':
                connection: HTTPConnection = HTTPConnection(host)
            else:
                connection: HTTPConnection = HTTPSConnection(host)
        except:
            return self._test_result(uri, URITest.REQUEST_FAIL)

        # TODO - Fix for http verb (ONLY HEAD RN)
        try:
            connection.request("HEAD", path, headers=self._headers())
        except:
            #     Add here
            print("Add")

        return self._test_result(uri, URITest.VALID_URI)
