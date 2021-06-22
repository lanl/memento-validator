from typing import List
from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.header_test import HeaderTest
from mementoweb.validator.tests.test import TestSetting, TestReport
from mementoweb.validator.tests.timegate_test import TimeGateTest
from mementoweb.validator.tests.uri_test import URITest


class TimeGate(DefaultPipeline):

    _tests: List[TestSetting] = [
        {'test': URITest(), 'params': None},
        {'test': TimeGateTest(), 'params': None}
    ]

    def validate(self, uri: str,
                 accept_datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:

        args = {
            "uri": uri
        }
        a = []

        a.append(URITest().test(**args))
        a.append(HeaderTest().test())
        # a.append(TimeGateTest().test(**args))

        return a
