from typing import List

from mementoweb.validator.tests.test import TestResult, TestSetting


class DefaultPipeline:
    _tests: List[TestSetting] = []

    def name(self) -> str:
        return self.__module__ + '.' + self.__class__.__name__

    def validate(self, uri: str,
                 accept_datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestResult]:
        uri = uri.strip()

        info = {
            'uri': uri.strip(),
            'accept-datetime': accept_datetime,
            'accept': accept
        }

        results = []

        for test_setting in self._tests:
            results.append(test_setting['test'].test(info, test_setting['params']))

        return results
