import json
import xml.etree.ElementTree as ElementTree
from typing import Union

from dotenv import dotenv_values

from mementoweb.apps.daily_validator.email_client import Email
from mementoweb.apps.daily_validator.email_report_generator import HTMLReportGenerator
from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timegate import TimeGate
from mementoweb.validator.pipelines.timemap import TimeMap


def _get_validator(validator_type: str) -> Union[DefaultPipeline, None]:
    if validator_type == "original":
        return Original()
    elif validator_type == "memento":
        return Memento()
    elif validator_type == "timemap":
        return TimeMap()
    elif validator_type == "timegate":
        return TimeGate()

    return None


if __name__ == '__main__':
    config = dotenv_values("daily-validator.env")
    archive_list_path: str = config.get("config", "config.xml")

    email_username: str = config.get("email-username", "username")
    email_password: str = config.get("email-password", "password")

    master_emails: str = config.get("master-emails", "prototeam@googlegroups.com")

    email_server = Email(username=email_username, password=email_password)

    tree = ElementTree.parse(archive_list_path)
    root = tree.getroot()

    report_generator = HTMLReportGenerator()
    master_report = ""

    links = root.findall(".//link")
    for link in links:
        name = link.get("longname")
        print("======================" + name + "======================")
        tests_node = link.find(".//tests")

        if tests_node:
            test_info_nodes = tests_node.findall(".//test")
            output_file = open("out/" + name + ".json", "w")
            for test_info in test_info_nodes:

                resource_type = test_info.attrib.pop("type")
                test_params = test_info.attrib
                validator = _get_validator(resource_type)

                if validator is None:
                    print("Invalid resource type")
                else:
                    result = validator.validate(**test_params)

                    html_report = report_generator.generate(test_params, result, name)
                    master_report = master_report + report_generator.generate(test_params, result, name,
                                                                              encapsulate_html=False)

                    if not html_report == "" and "email" in tests_node.attrib.keys():
                        emails = tests_node.attrib["email"].split(",")
                        email_server.send_email(receiver=emails,
                                                subject=name + " - Daily Validator Report -",
                                                html_message=html_report)
                        print("Email notifications sent to : " + ",".join(emails))
                    json.dump({
                        "type": resource_type,
                        "params": test_params,
                        "pipeline": validator.name(),
                        "results": [report.to_json() for report in result.reports]
                    }, output_file, ensure_ascii=False, indent=4)
            output_file.close()


    email_server.send_email(receiver=master_emails.split(","), subject="Daily Validator Report",
                            html_message=report_generator._html_start_text + master_report + report_generator._html_end_text)
