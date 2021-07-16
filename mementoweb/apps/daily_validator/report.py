from typing import List

from mementoweb.validator.tests.test import TestReport, TestResult


def _params_to_html(params: dict):
    html = """<h4> Daily Validator Parameters</h4>
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


def _test_to_html(test: TestResult):
    return """
    <tr>
        <td>""" + test.name + """</td>
        <td>""" + test.result() + """</td>
    </tr>
    """


def _report_to_html(report: TestReport):
    return """
        <h3>""" + report.name.split(".")[-1] + """</h3>
        <table style="width:100%">
          <tr>
            <th colspan="2">""" + report.description + """</th>
          </tr>
          """ + " ".join([_test_to_html(test) for test in report.tests]) + """
        </table>
        <small>""" + report.name + """</small>
        <br>
    """


def generate_html(test_parameters: dict,
                  reports: List[TestReport]):
    html_text = """
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

    filtered_reports: List[TestReport] = \
        list(filter(lambda report: any(test.status == TestResult.TEST_FAIL for test in report.tests), reports))

    if len(filtered_reports) == 0:
        return ""

    for report in filtered_reports:
        report.tests = list(filter(lambda test: test.status == TestResult.TEST_FAIL, report.tests))
        html_text += _report_to_html(report)

    if len(test_parameters) > 0:
        html_text += _params_to_html(test_parameters)

    return html_text + """
        </body>
        </html>
    """
