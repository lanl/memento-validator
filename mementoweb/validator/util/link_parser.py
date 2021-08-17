import re


class LinkParserResult:
    uri: str = ""

    relationship: str = ""

    link_type: str = ""

    datetime: str = ""

    title: str = ""

    link_from: str = ""

    link_until: str = ""

    def __init__(self, uri: str = "",
                 relationship: str = "",
                 link_type: str = "",
                 datetime: str = "",
                 title: str = "",
                 link_from: str = "",
                 link_until: str = ""):
        self.uri = uri
        self.relationship = relationship
        self.datetime = datetime
        self.link_type = link_type
        self.title = title
        self.link_from = link_from
        self.link_until = link_until


class LinkParser:

    def parse(self, link_header: str) -> [LinkParserResult]:
        pass


class RegexLinkParser(LinkParser):
    _split_point = ""

    def __init__(self, split_point="[,]\s*[<]"):
        self._split_point = split_point

    def parse(self, link_header: str) -> [LinkParserResult]:
        link_header = link_header.strip()

        _link_parser_result = []

        split_point = re.compile(self._split_point)

        link_header_splits = [x.replace('>', '').replace('<', '') for x in split_point.split(link_header)]
        # link_header_splits = [x.replace('>', '').replace('<', '') for x in link_header.split(', <')]

        for item in link_header_splits:
            # relationship is mandatory
            relationships = re.findall('((?<=rel=")[^"]*)', item)

            # Append only if theres relationship
            if relationships:
                link = item.split(";")[0]
                relationship = relationships[0].strip()

                link_type = (re.findall('((?<=type=")[^"]*)', item) or [""])[0]
                datetime = (re.findall('((?<=datetime=")[^"]*)', item) or [""])[0]
                link_from = (re.findall('((?<=from=")[^"]*)', item) or [""])[0]
                link_until = (re.findall('((?<=until=")[^"]*)', item) or [""])[0]
                # License needed ??
                # lic = (re.findall('((?<=license=")[^"]*)', item) or [""])[0]

                _link_parser_result.append(
                    LinkParserResult(uri=link, relationship=relationship, datetime=datetime, link_type=link_type,
                                     link_from=link_from, link_until=link_until)
                )

        return _link_parser_result


class CharacterLinkParser(LinkParser):

    def parse(self, link_header: str) -> [LinkParserResult]:
        state = 'start'
        link_header = link_header.strip()
        data = [d for d in link_header]
        links = {}

        while data:
            if state == 'start':
                d = data.pop(0)
                while d.isspace():
                    d = data.pop(0)
                if d != "<":
                    # raise ValueError("Expected < in start, got %s" % d)
                    return self._transform({})
                state = "uri"
            elif state == "uri":
                uri = []
                d = data.pop(0)
                while d != ">":
                    uri.append(d)
                    d = data.pop(0)
                uritmp = ['>']
                if not data:
                    return self._transform({})
                d = data.pop(0)
                while d.isspace():
                    uritmp.append(d)
                    d = data.pop(0)
                if d in [',', ';']:
                    uri = ''.join(uri)
                    # uri = uri[:-1]
                    # Not an error to have the same URI multiple times (I think!)
                    if not uri in links.keys():
                        links[uri] = {}
                    state = "paramstart"
                else:
                    uritmp.append(d)
                    uri.extend(uritmp)

            elif state == 'paramstart':
                # d = data.pop(0)
                while data and d.isspace():
                    d = data.pop(0)
                if d == ";":
                    state = 'linkparam'
                elif d == ',':
                    state = 'start'
                else:
                    return self._transform({})
                    # raise ValueError("Expected ; in paramstart, got %s" % d)
            elif state == 'linkparam':
                d = data.pop(0)
                while d.isspace():
                    d = data.pop(0)
                paramType = []
                while not d.isspace() and d != "=":
                    paramType.append(d)
                    d = data.pop(0)
                while d.isspace():
                    d = data.pop(0)
                if d != "=":
                    return {}
                    # raise ValueError("Expected = in linkparam, got %s" % d)
                state = 'linkvalue'
                pt = ''.join(paramType)
                if not pt in links[uri].keys():
                    links[uri][pt] = []
            elif state == 'linkvalue':
                d = data.pop(0)
                while d.isspace():
                    d = data.pop(0)
                paramValue = []
                if d == '"':
                    pd = d
                    d = data.pop(0)
                    while d != '"' and pd != '\\':
                        paramValue.append(d)
                        pd = d
                        d = data.pop(0)
                else:
                    while not d.isspace() and not d in (',', ';'):
                        paramValue.append(d)
                        if data:
                            d = data.pop(0)
                        else:
                            break
                    if data:
                        data.insert(0, d)
                state = 'paramstart'
                if data:
                    d = data.pop(0)
                pv = ''.join(paramValue)
                if pt == 'rel':
                    # rel types are case insensitive and space separated
                    links[uri][pt].extend([y.lower() for y in pv.split(' ')])
                else:
                    if not pv in links[uri][pt]:
                        links[uri][pt].append(pv)

        return self._transform(links)

    def _transform(self, links: dict) -> [LinkParserResult]:
        _link_parser_results = []

        for key in links.keys():
            value: dict = links[key]
            _link_parser_results.append(
                LinkParserResult(uri=key, relationship=value.get("rel", [""])[0], link_type=value.get("type", [""])[0],
                                 title=value.get("title", [""])[0])
            )

        return _link_parser_results


class MemgatorParser(LinkParser):

    def parse(self, link_header: str) -> [LinkParserResult]:
        # TODO - Transfer froom memegator
        return LinkParserResult()
