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

import click
import textwrap


from mementoweb.validator.pipelines import TimeGate, DefaultPipeline
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timemap import TimeMap


def run(uri, resource_type, datetime):
    """

    Provides entry point for the CLI-validator interface.
    :param uri: URI of the resource being tested.
    :param resource_type: Type of the resource (original, memento, timegate, or timemap)
    :param datetime: Datetime for validating the resource (Should follow BNF format)
    :return: None. Displays the results in the console.

    """

    validator: DefaultPipeline = None

    if resource_type == "timegate":
        validator = TimeGate()
    if resource_type == "memento":
        validator = Memento()
    if resource_type == "timemap":
        validator = TimeMap()
    if resource_type == "original":
        validator = Original()

    if validator is None:
        print("Invalid Validator")
        return
    else:
        result = validator.validate(uri, datetime)
        for report in result.reports:
            print("="*99)
            # print("{:<15} | {:<80}|".format('Source', textwrap.shorten(report.name.split(".")[-1], width=75)))
            print("{:<98}|".format(textwrap.shorten(report.name, width=98)))
            print("{:<98}|".format(textwrap.shorten(report.description, width=98)))

            print("="*60+" + "+"="*36)
            # print("{:<60} | {:<35}|".format('Test Name', 'Status'))
            # print("="*60+" + "+"="*36)
            for test in report.tests:
                print("{:<60} | {:<35}|".format(textwrap.shorten(test.name(), width=60), test.result()))
            print("-"*60+" + "+"-"*36+"\n")




@click.command()
@click.option("--uri", help="URI of the resource")
@click.option("--type", "type_",
              type=click.Choice(["original", "memento", "timemap", "timegate"], case_sensitive=False),
              help="Type of resource")
@click.option("--date", default="Sun, 01 Apr 2010 12:00:00 GMT", help="Date Time for testing the resource")
def cli(uri, type_, date):
    run(uri, type_, date)


if __name__ == '__main__':
    cli()
