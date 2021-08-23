from typing import List

from typing_extensions import TypedDict

from mementoweb.validator.util.http import HttpConnection


class TestResult:
    """

    Abstraction of a test result/ single test

    """
    TEST_PASS: int = 2

    TEST_WARN: int = 1

    TEST_FAIL: int = -1

    TEST_INFO: int = 0

    _name: str

    _status: int

    _description: str

    def __init__(self, name: str = "", status: int = TEST_FAIL, description: str = ""):
        self._name = name
        self._description = description
        self._status = status

    def result(self) -> str:
        if self._status == self.TEST_PASS:
            return "Pass"
        if self._status == self.TEST_INFO:
            return "Info"
        if self._status == self.TEST_WARN:
            return "Warn"
        else:
            return "Fail"

    def name(self):
        return self._name

    def to_json(self):
        return {
            "name": self._name,
            "description": self._description,
            "status": self._status,
            "result": self.result()
        }


class TestReport:
    """

    Abstraction to a test report/ results of collection of tests

    """
    REPORT_PASS: int = 1

    REPORT_WARN: int = 0

    REPORT_FAIL: int = -1

    report_status: int

    name: str

    description: str

    tests: List[TestResult]

    def __init__(self, report_status: int = REPORT_FAIL, description: str = "", name: str = "",
                 tests: List[TestResult] = None):
        self.report_status = report_status
        self.description = description
        self.name = name
        if tests is None:
            tests = []
        self.tests = tests

    def result(self) -> str:
        if self.report_status == self.REPORT_PASS:
            return "Pass"
        if self.report_status == self.REPORT_WARN:
            return "Warn"
        else:
            return "Fail"

    def to_json(self) -> dict:
        return {
            "name": self.name.split(".")[-1],
            "source": self.name,
            "description": self.description,
            "status": self.report_status,
            "result": self.result(),
            "tests": [test.to_json() for test in self.tests]
        }


class TestInfo(TypedDict):
    uri: str

    connection: HttpConnection


class BaseTest:
    """

    Abstraction for a test

    """
    _description: str = "No description"

    _test_report: TestReport

    _headers = {
        'Accept-Datetime': 'Thu, 10 Oct 2009 12:00:00 GMT',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2'
    }

    def __init__(self):
        self._test_report = TestReport(
            name=self._name(),
            description=self._description,
            report_status=TestReport.REPORT_FAIL,
            tests=[]
        )

    def test(self, **kwargs: dict) -> TestReport:
        """

        Perform the test the specified test need to perform

        :param **kwargs:
        :return: List[TestResult]

        """
        pass

    def add_test_result(self, test_result: TestResult):
        self._test_report.tests.append(test_result)

    def _name(self) -> str:
        return self.__module__ + '.' + self.__class__.__name__

