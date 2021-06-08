from typing import TypedDict

TEST_PASS: int = 1

TEST_FAIL: int = 0


class TestResult(TypedDict):
    type: str

    description: str

    uri: str


class BaseTest:
    _headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2'
    }

    def test(self, info: dict, params: dict = dict()) -> TestResult:
        pass

    def _test_result(self, uri: str, description: str) -> TestResult:
        return {
            'name': self._name(),
            'uri': uri,
            'description': description
        }

    def _name(self) -> str:
        return self.__module__ + '.' + self.__class__.__name__


class TestSetting(TypedDict):

    params: dict

    test: BaseTest
