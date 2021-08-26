#
#  Copyright (c) 2021. Los Alamos National Laboratory (LANL).
#  Written by: Bhanuka Mahanama (bhanuka@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  Correspondence: Lyudmila Balakireva, PhD (ludab@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  See LICENSE in the project root for license information.
#

import re
from http.client import HTTPConnection, HTTPSConnection, HTTPResponse
from typing import List
from urllib.parse import ParseResult, urlparse

from mementoweb.validator.errors.header_errors import HeadersNotFoundError, LinkHeaderNotFoundError, \
    HeaderTypeNotFoundError, HeaderParseError
from mementoweb.validator.errors.uri_errors import HttpRequestFailError, HttpConnectionFailError, InvalidUriError
from mementoweb.validator.util.link_parser import LinkParser, RegexLinkParser, LinkParserResult

"""
    
    Http related functions and classes - Isolate the urlib (for any issues/ changes in future versions)
    Used as an adapter in the package 
    
"""


class HttpResponse:
    """

        An adapter class for isolating urlib incase of future changes/ issues. Encapsulates HTTP response from an established
        connection.

    """
    _response: HTTPResponse = None

    _headers = None

    _link_headers: [LinkParserResult] = None

    status = None

    body = None

    link_parser: LinkParser = RegexLinkParser()

    def __init__(self, response: HTTPResponse = None, uri=""):
        self.uri = uri
        self._response = response
        self._headers = dict(self._response.getheaders())
        self.status = response.status
        self.body = response.read().decode('utf-8')

    def search_link_headers(self, relationship: str, regex=False) -> [LinkParserResult]:
        try:
            if self._link_headers is None:
                self._link_headers = self.link_parser.parse(self.get_headers("Link"))
            if not regex:
                return [x for x in self._link_headers if x.relationship == relationship]
            else:
                return list(filter(lambda x: re.findall(relationship, x.relationship), self._link_headers))
        except HeadersNotFoundError:
            raise HeadersNotFoundError()
        except HeaderTypeNotFoundError:
            raise LinkHeaderNotFoundError()
        except Exception:
            raise HeaderParseError()

    def get_headers(self, name: str) -> str:
        if not self._headers:
            raise HeadersNotFoundError()
        if name in self._headers.keys():
            return self._headers[name]
        else:
            raise HeaderTypeNotFoundError()

    def header_keys(self) -> List:
        return list(self._headers.keys())

    def get_body(self):
        return self.body

    def parse_body(self):
        return self.link_parser.parse(self.body.replace("\n", ""))


class HttpConnection:
    """

        An adapter class for HTTPConnection. Used for isolating urlib incase of issues in the future.

    """

    _connection: HTTPConnection = None

    _response: HttpResponse = None

    _uri: str = None

    def __init__(self, host, scheme, uri):
        self._uri = uri
        if scheme == 'http':
            self._connection = HTTPConnection(host)
        else:
            self._connection = HTTPSConnection(host)

    def request(self, method, path, headers):
        self._connection.request(method, path, headers=headers)
        self._response = HttpResponse(self._connection.getresponse(), uri=self._uri)

    def get_response(self) -> HttpResponse:
        return self._response


def http(uri: str,
         datetime='Thu, 10 Oct 2009 12:00:00 GMT',
         accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         accept_language='en-us,en;q=0.5',
         proxy_connection='keep-alive',
         user_agent='Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2',
         method='HEAD'
         ) -> HttpConnection:
    """

    Initiates HTTP connections using the given parameters using the HTTP Adapter.

    :param uri: URI for the connection
    :param datetime: Datetime for Accept-Datetime header
    :param accept: Content type for Accept header
    :param accept_language: language for Accept-Language head
    :param proxy_connection: value for Proxy-Connection header
    :param user_agent: User-Agent header
    :param method:request method. Defaults to HEAD.
    :return: HTTP connection using the given parameters.
    """
    headers = {
        'Accept-Datetime': datetime,
        'Accept': accept,
        'Accept-Language': accept_language,
        'Proxy-Connection': proxy_connection,
        'User-Agent': user_agent
    }

    params: ParseResult = urlparse(url=uri)

    host: str = params.netloc
    if params.port == 80:
        # required??
        host = params.netloc.replace(':80', '')

    if not host:
        raise InvalidUriError()

    path = params.path

    if path and path[0] != '/':
        path = '/' + path

    if not params.query:
        path = path + "?" + params.query

    try:
        if params.scheme == 'http':
            connection: HttpConnection = HttpConnection(host, params.scheme, uri=uri)
        else:
            connection: HttpConnection = HttpConnection(host, params.scheme, uri=uri)
    except:
        raise HttpConnectionFailError()

    try:
        connection.request(method, path, headers=headers)
    except Exception as ex:
        raise HttpRequestFailError()

    return connection
