# Memento Validator
Memento validator toolkit lets you validate your memento implementation.
Toolkit includes
1. Web API
2. Web GUI
3. Validation CLI

## 1. Web API

You can either host the web API locally (for testing local URIs), or can use 
the hosted instance at `http://labs.mementoweb.org/validator/`.

### API Specification

**[GET] /**

| Parameter     |  Description | Example  |
|---            |---|---|
| uri           | URI of the resource  | ```https://arquivo.pt/wayback/20080215125110/http://www.facebook.com/``` |
| datetime      | Date and time for validating resource | ```Sun, 01 Apr 2010 12:00:00 GMT```  |
| type          | Type of the resource to validate   | ```timegate``` or ```memento``` or ```timemap``` or ```original```|
| followLinks   | Flag for follow-up tests. Default ```False``` | ```True``` or ```False``` |

Example: 

```shell
curl 'http://labs.mementoweb.org/validator/?datetime=Sun,%2001%20Apr%202010%2012:00:00%20GMT&uri=http://webarchive.parliament.uk/timegate/http://animatingcardiff.wordpress.com&type=timegate&followLinks=false'
```

```json
{"datetime":"Sun, 01 Apr 2010 12:00:00 GMT","pipeline":"mementoweb.validator.pipelines.timegate.TimeGate","results":[{"description":"Tests for the validity of the URI of the resource including validity and connectivity","name":"URITest","result":"Pass","source":"mementoweb.validator.tests.uri_test.URITest","status":1,"tests":[{"description":"","name":"Valid URI","result":"Pass","status":2}]},{"description":"Tests for the timegate redirection. Checks for any redirection and tests for the validity","name":"TimeGateRedirectTest","result":"Pass","source":"mementoweb.validator.tests.timegate_redirect_test.TimeGateRedirectTest","status":1,"tests":[{"description":"","name":"TimeGate returns 302","result":"Pass","status":2}]},{"description":"No description","name":"HeaderTest","result":"Pass","source":"mementoweb.validator.tests.header_test.HeaderTest","status":1,"tests":[{"description":"","name":"Location Header found","result":"Pass","status":2},{"description":"","name":"Accept-Datetime not in vary header","result":"Fail","status":-1}]},{"description":"No description","name":"LinkHeaderTimeMapTest","result":"Pass","source":"mementoweb.validator.tests.link_header_timemap_test.LinkHeaderTimeMapTest","status":1,"tests":[{"description":"","name":"Timemap link present","result":"Pass","status":2},{"description":"","name":"Timemap type present","result":"Pass","status":2}],"timemaps":["http://webarchive.parliament.uk/timemap/*/http://animatingcardiff.wordpress.com"]},{"description":"No description","name":"LinkHeaderMementoTest","result":"Pass","source":"mementoweb.validator.tests.link_header_memento_test.LinkHeaderMementoTest","status":1,"tests":[{"description":"","name":"Memento link present","result":"Pass","status":2},{"description":"","name":"Selected memento not in link header","result":"Warn","status":1},{"description":"","name":"Memento contains datetime attribute","result":"Pass","status":2},{"description":"","name":"Memento datetime parsable","result":"Pass","status":2}]},{"description":"Tests for the timegate redirection. Checks for any redirection and tests for the validity","name":"TimeGateRedirectTest-blank","result":"Fail","source":"mementoweb.validator.tests.timegate_redirect_test.TimeGateRedirectTest-blank","status":-1,"tests":[{"description":"","name":"TimeGate returns 302 for datetime in future","result":"Pass","status":2}]},{"description":"Tests for the timegate redirection. Checks for any redirection and tests for the validity","name":"TimeGateRedirectTest-past","result":"Fail","source":"mementoweb.validator.tests.timegate_redirect_test.TimeGateRedirectTest-past","status":-1,"tests":[{"description":"","name":"TimeGate returns 302 for datetime in past","result":"Pass","status":2}]},{"description":"Tests for the timegate redirection. Checks for any redirection and tests for the validity","name":"TimeGateRedirectTest-future","result":"Fail","source":"mementoweb.validator.tests.timegate_redirect_test.TimeGateRedirectTest-future","status":-1,"tests":[{"description":"","name":"TimeGate returns 302 for datetime in future","result":"Pass","status":2}]},{"description":"Tests for the timegate redirection. Checks for any redirection and tests for the validity","name":"TimeGateRedirectTest-broken","result":"Fail","source":"mementoweb.validator.tests.timegate_redirect_test.TimeGateRedirectTest-broken","status":-1,"tests":[{"description":"","name":"Timegate does not return 400 for broken datetime","result":"Fail","status":-1}]}],"type":"timegate","uri":"http://webarchive.parliament.uk/timegate/http://animatingcardiff.wordpress.com"}
```

### Setup Instructions

1. Install Dependencies

```shell
$ pip install -r requirements.txt
```

2. Export Flask Module (REMOVE)

```shell
$ export FLASK_APP=mementoweb/validator/web/server.py
```

3. Run Server (Add Port and config)

```shell
$ flask run
```

## Web Front-end

### Installation Instructions

## CLI Tool

## Package Installation (ADD)

## Documentation

### API Documentation

### Package Documentation
Generate documentation
```shell
$ cd docs

$ sphinx-apidoc -o source ..

$ make html
```

```shell
$ firefox build/html/index.html
```
