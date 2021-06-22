from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.test import TestReport
from mementoweb.validator.tests.uri_test import URITest


class TimeGate(DefaultPipeline):

    def validate(self, uri: str,
                 accept_datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:

        results = [URITest().test(uri=uri)]

        # results.append(LinkHeaderTest().test())
        # a.append(TimeGateTest().test(**args))

        return results
