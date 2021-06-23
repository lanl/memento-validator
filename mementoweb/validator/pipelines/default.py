from typing import List

from mementoweb.validator.tests.test import TestReport


class DefaultPipeline:

    def name(self) -> str:
        return self.__module__ + '.' + self.__class__.__name__

    def validate(self,
                 uri: str,
                 accept_datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> List[TestReport]:
        pass
