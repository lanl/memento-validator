from http.client import HTTPConnection, HTTPSConnection
from typing import List
from urllib.parse import urlparse, ParseResult

from mementoweb.validator.errors.uri_errors import InvalidUriError, HttpRequestFailError, HttpConnectionFailError


def http(uri: str,
         datetime='Thu, 10 Oct 2009 12:00:00 GMT',
         accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         accept_language='en-us,en;q=0.5',
         proxy_connection='keep-alive',
         user_agent='Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2',
         method='HEAD'
         ) -> HTTPConnection:
    headers = {
        'Accept-Datetime': datetime,
        'Accept': accept,
        'Accept-Language': accept_language,
        'Proxy-Connection': proxy_connection,
        'User-Agent': user_agent
    }

    params: ParseResult = urlparse(url=uri)

    # TODO - Check tuple handling validatorhandler 212 (Python 2.4 fix??)
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
            connection: HTTPConnection = HTTPConnection(host)
        else:
            connection: HTTPConnection = HTTPSConnection(host)
    except:
        raise HttpConnectionFailError()

    try:
        connection.request(method, path, headers=headers)
    except Exception as ex:
        raise HttpRequestFailError()

    return connection


def parse_link_header(link_header: str) -> dict:
    link_header = link_header.strip()
    link_info = dict()
    hdr_info = [x.replace('>', '').replace('<', '') for x in link_header.split(', <')]

    for item in hdr_info:
        link = item.split(";")[0]
        desc = item.split(";", 1)[1].replace("\"", "")

        if link in link_info.keys():
            link_info[link] = link_info[link] + ";" + desc
        else:
            link_info[link] = desc

    return link_info


def search_link_headers(link_header_info, rel) -> List[str]:
    links = []

    for link, link_info in link_header_info.items():
        if rel in link_info:
            links.append(link)

    return links
