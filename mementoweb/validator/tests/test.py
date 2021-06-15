from typing import List

from typing_extensions import TypedDict

TEST_PASS: int = 1

TEST_WARN: int = 0

TEST_FAIL: int = -1


class TestResult(TypedDict):
    """
    Attributes to a test result
    """
    status: int

    type: str

    description: str

    uri: str


class BaseTest:

    _headers = {
        'Accept-Datetime': 'Thu, 10 Oct 2009 12:00:00 GMT',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2'
    }

    def test(self, info: dict, params: dict = None) -> List[TestResult]:
        """
        Perform the test the specified test need to perform

        :param info: information passed from the pipeline
        :param params: test specific params in the pipeline
        :return: List[TestResult]
        """
        pass

    def _test_result(self, uri: str, description: str, test_status: int = TEST_FAIL) -> TestResult:
        return {
            'status': test_status,
            'name': self._name(),
            'uri': uri,
            'description': description
        }

    def _name(self) -> str:
        return self.__module__ + '.' + self.__class__.__name__


class TestSetting(TypedDict):

    params: dict

    test: BaseTest
