#
#  Copyright (c) 2021. Los Alamos National Laboratory (LANL).
#  Written by: Bhanuka Mahanama (bhanuka@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  Correspondence: Lyudmila Balakireva, PhD (ludab@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  See LICENSE in the project root for license information.
#

import logging
import os
import xml.etree.ElementTree as ElementTree
from distutils.util import strtobool
from typing import Union

import click
from dotenv import dotenv_values

from mementoweb.apps.daily_validator.email_client import Email, SecureEmail, UnsecureEmail, EmailServerError
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


def run(file_name="daily-validator.env"):
    """

    Provides an entry point for the Daily Validator interface. Used by the command line tool or when invoked.

    :param file_name: File containing the configurations for the daily validator.
    :return: None

    """

    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(file_name):
        logging.warning(file_name + " not found. Loading from default values.")

    config = dotenv_values(file_name)

    archive_list_path: str = config.get("config", "config.xml")

    email_server: Email

    email_host: str = config.get("email-host", "localhost")
    email_port: int = int(config.get("email-port", 0))

    secure_email: bool = strtobool(config.get("secure-email", "False"))
    try:
        if secure_email:
            email_username: str = config.get("email-username", "username")
            email_password: str = config.get("email-password", "password")
            email_server = SecureEmail(username=email_username, password=email_password, host=email_host,
                                       port=email_port)
        else:
            email_server = UnsecureEmail(port=email_port, host=email_host)
    except EmailServerError:
        logging.error("Unable to connect to email host " + email_host + " port " + str(email_port))
        return

    master_emails: str = config.get("master-emails")

    tree = ElementTree.parse(archive_list_path)
    root = tree.getroot()

    report_generator = HTMLReportGenerator()
    master_report = ""

    links = root.findall(".//link")
    for link in links:
        name = link.get("longname")
        logging.info("Starting tests for archive: " + name)
        tests_node = link.find(".//tests")

        if tests_node:
            test_info_nodes = tests_node.findall(".//test")
            # output_file = open("out/" + name + ".json", "w")
            for test_info in test_info_nodes:

                resource_type = test_info.attrib.pop("type")
                test_params = test_info.attrib
                validator = _get_validator(resource_type)

                if validator is None:
                    logging.error("Invalid resource type " + resource_type + " for " + name)
                else:
                    logging.info("Testing" + resource_type + " with parameters " + test_params.__str__())
                    result = validator.validate(**test_params)

                    html_report = report_generator.generate(test_params, result, name)
                    master_report = master_report + report_generator.generate(test_params, result, name,
                                                                              encapsulate_html=False)

                    if not html_report == "" and "email" in tests_node.attrib.keys():
                        emails = tests_node.attrib["email"].split(",")
                        email_server.send_email(receiver=emails,
                                                subject=name + " - Daily Validator Report -",
                                                html_message=html_report)
                        logging.info("Email notifications sent to : " + ",".join(emails))
            #         json.dump({
            #             "type": resource_type,
            #             "params": test_params,
            #             "pipeline": validator.name(),
            #             "results": [report.to_json() for report in result.reports]
            #         }, output_file, ensure_ascii=False, indent=4)
            # output_file.close()

        logging.info("Ending tests for archive: " + name)

    if master_emails is not None:
        email_server.send_email(receiver=master_emails.split(","), subject="Daily Validator Report",
                                html_message=report_generator._html_start_text + master_report + report_generator._html_end_text)


@click.command()
@click.option("--env", default="daily-validator.env", help="Location of the .env configuration")
def daily(env):
    run(env)


if __name__ == '__main__':
    daily()
