HTTP API
======================================

.. image:: ../_static/http-api.png


You can either host the web API locally (for testing local URIs), or can use
the LANL hosted instance at `http://labs.mementoweb.org/validator/api`.

API Specification
-----------------
**[GET] /**

+---------------+-----------------------------------------------+
| Parameter     |  Description                                  |
+===============+===============================================+
| uri           | URI of the resource                           |
+---------------+-----------------------------------------------+
| datetime      | Date and time for validating resource         |
+---------------+-----------------------------------------------+
| type          | Type of the resource to validate              |
+---------------+-----------------------------------------------+
| followLinks   | Flag for follow-up tests. Default ```False``` |
+---------------+-----------------------------------------------+

Example:

""
>> curl 'http://labs.mementoweb.org/validator/api?datetime=Sun,%2001%20Apr%202010%2012:00:00%20GMT&uri=http://webarchive.parliament.uk/timegate/http://animatingcardiff.wordpress.com&type=timegate&followLinks=false'
""

""
{
    "datetime": "Sun, 01 Apr 2010 12:00:00 GMT",
    "follow": {},
    "pipeline": "mementoweb.validator.pipelines.timegate.TimeGate",
    "result": {
        "reports": [
            {
                "description": "Tests for the validity of the URI of the resource including validity and connectivity.",
                "name": "URITest",
                "source": "mementoweb.validator.tests.uri_test.URITest",
                "tests": [
                    {
                        "description": "",
                        "name": "Valid URI",
                        "result": "Pass",
                        "status": 2
                    }
                ]
            },
            {
                "description": "Tests for the timegate redirection. Checks for any redirection and tests for the validity",
                "name": "TimeGateRedirectTest",
                "source": "mementoweb.validator.tests.timegate_redirect_test.TimeGateRedirectTest",
                "tests": [
                    {
                        "description": "",
                        "name": "TimeGate returns 302",
                        "result": "Pass",
                        "status": 2
                    }
                ]
            },
            {
                "description": "No description",
                "name": "HeaderTest",
                "source": "mementoweb.validator.tests.header_test.HeaderTest",
                "tests": [
                    {
                        "description": "",
                        "name": "Location Header found",
                        "result": "Pass",
                        "status": 2
                    },
                    {
                        "description": "",
                        "name": "Accept-Datetime not in Vary header",
                        "result": "Fail",
                        "status": -1
                    }
                ]
            },
            {
                "description": "Tests for the compliance of Link header original relation.",
                "name": "LinkHeaderOriginalTest",
                "source": "mementoweb.validator.tests.link_header_original_test.LinkHeaderOriginalTest",
                "tests": [
                    {
                        "description": "",
                        "name": "Original link present",
                        "result": "Pass",
                        "status": 2
                    }
                ]
            },
            {
                "description": "Tests the compliance of Link header timemap relation.",
                "name": "LinkHeaderTimeMapTest",
                "source": "mementoweb.validator.tests.link_header_timemap_test.LinkHeaderTimeMapTest",
                "tests": [
                    {
                        "description": "",
                        "name": "Timemap link present",
                        "result": "Pass",
                        "status": 2
                    },
                    {
                        "description": "",
                        "name": "Timemap type present",
                        "result": "Pass",
                        "status": 2
                    }
                ],
                "timemaps": [
                    "http://webarchive.parliament.uk/timemap/*/http://animatingcardiff.wordpress.com"
                ]
            },
            {
                "description": "Tests for the compliance of Link header memento relation.",
                "name": "LinkHeaderMementoTest",
                "source": "mementoweb.validator.tests.link_header_memento_test.LinkHeaderMementoTest",
                "tests": [
                    {
                        "description": "",
                        "name": "Memento link present",
                        "result": "Pass",
                        "status": 2
                    },
                    {
                        "description": "",
                        "name": "Selected memento not in link header",
                        "result": "Warn",
                        "status": 1
                    },
                    {
                        "description": "",
                        "name": "Memento contains datetime attribute",
                        "result": "Pass",
                        "status": 2
                    },
                    {
                        "description": "",
                        "name": "Memento datetime parsable",
                        "result": "Pass",
                        "status": 2
                    },
                    {
                        "description": "",
                        "name": "First Memento does not match first in the Timemap",
                        "result": "Warn",
                        "status": 1
                    },
                    {
                        "description": "",
                        "name": "Last Memento does not match last in the Timemap",
                        "result": "Warn",
                        "status": 1
                    }
                ]
            },
            {
                "description": "Tests for the timegate redirection. Checks for any redirection and tests for the validity",
                "name": "TimeGateBlankRedirectTest",
                "source": "mementoweb.validator.tests.timegate_redirect_test.TimeGateBlankRedirectTest",
                "tests": [
                    {
                        "description": "",
                        "name": "TimeGate returns 200 or redirect for blank Accept-Datetime",
                        "result": "Pass",
                        "status": 2
                    },
                    {
                        "description": "",
                        "name": "TimeGate redirects to last memento without Accept-Datetime",
                        "result": "Pass",
                        "status": 2
                    }
                ]
            },
            {
                "description": "Tests for the timegate redirection. Checks for any redirection and tests for the validity",
                "name": "TimeGatePastRedirectTest",
                "source": "mementoweb.validator.tests.timegate_redirect_test.TimeGatePastRedirectTest",
                "tests": [
                    {
                        "description": "",
                        "name": "TimeGate returns 302 for datetime in past",
                        "result": "Pass",
                        "status": 2
                    },
                    {
                        "description": "",
                        "name": "TimeGate redirects to first memento for datetime in past",
                        "result": "Pass",
                        "status": 2
                    }
                ]
            },
            {
                "description": "Tests for the timegate redirection. Checks for any redirection and tests for the validity",
                "name": "TimeGateFutureRedirectTest",
                "source": "mementoweb.validator.tests.timegate_redirect_test.TimeGateFutureRedirectTest",
                "tests": [
                    {
                        "description": "",
                        "name": "TimeGate returns 302 for datetime in future",
                        "result": "Pass",
                        "status": 2
                    },
                    {
                        "description": "",
                        "name": "TimeGate redirects to first memento for datetime in past",
                        "result": "Pass",
                        "status": 2
                    }
                ]
            },
            {
                "description": "Tests for the timegate redirection. Checks for any redirection and tests for the validity",
                "name": "TimeGateBrokenRedirectTest",
                "source": "mementoweb.validator.tests.timegate_redirect_test.TimeGateBrokenRedirectTest",
                "tests": [
                    {
                        "description": "",
                        "name": "Timegate does not return 400 for broken datetime",
                        "result": "Fail",
                        "status": -1
                    }
                ]
            }
        ],
        "timegates": [],
        "timemaps": [
            "http://webarchive.parliament.uk/timemap/*/http://animatingcardiff.wordpress.com"
        ]
    },
    "type": "timegate",
    "uri": "http://webarchive.parliament.uk/timegate/http://animatingcardiff.wordpress.com"
}
""