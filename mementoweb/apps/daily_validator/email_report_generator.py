from typing import List

from mementoweb.validator.pipelines.default import PipelineResult
from mementoweb.validator.tests.test import TestReport, TestResult


class HTMLReportGenerator:
    _html_start_text = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        th, td {
          padding: 5px;
          text-align: left;    
        }
        </style>
        </head>
        <body>
    
        """

    _html_end_text = """
            </body>
            </html>
        """

    def generate(self, test_parameters: dict,
                 result: PipelineResult,
                 name: str,
                 encapsulate_html: bool = True,
                 start_text: str = ""):

        filtered_reports: List[TestReport] = \
            list(filter(lambda report: any(test.status == TestResult.TEST_FAIL for test in report.tests), result.reports))

        if len(filtered_reports) == 0:
            return ""
        start_text = "<h3>" + name + "</h3>"

        for filtered_report in filtered_reports:
            filtered_report.tests = list(filter(lambda test: test.status == TestResult.TEST_FAIL, filtered_report.tests))
            start_text += self._report_to_html(filtered_report)

        if len(test_parameters) > 0:
            start_text += self._params_to_html(test_parameters)

        if encapsulate_html:
            return self._html_start_text + start_text + self._html_end_text

        return start_text + "<hr>"

    def _params_to_html(self, params: dict):
        html = """<h5> Daily Validator Parameters</h5>
            <table style="width:100%">
        """
        for key in params.keys():
            html += """
                <tr>
                    <td>""" + key + """</td>
                    <td>""" + params[key] + """</td>
                </tr>
            """

        return html + "</table>"

    def _test_to_html(self, test: TestResult):
        return """
        <tr>
            <td>""" + test.name + """</td>
            <td>""" + test.result() + """</td>
        </tr>
        """

    def _report_to_html(self, report: TestReport):
        return """
            <h4>""" + report.name.split(".")[-1] + """</h4>
            <table style="width:100%">
              <tr>
                <th colspan="2">""" + report.description + """</th>
              </tr>
              """ + " ".join([self._test_to_html(test) for test in report.tests]) + """
            </table>
            <small>""" + report.name + """</small>
            <br>
        """
