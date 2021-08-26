import os
from pprint import pprint
import textwrap
import click

from mementoweb.validator.pipelines import TimeGate, DefaultPipeline
from mementoweb.validator.pipelines.memento import Memento
from mementoweb.validator.pipelines.original import Original
from mementoweb.validator.pipelines.timemap import TimeMap


class CliHandler:
    _original: Original

    _memento: Memento

    _timemap: TimeMap

    _timegate: TimeGate

    def __init__(self):
        self._original = Original()
        self._memento = Memento()
        self._timemap = TimeMap()
        self._timegate = TimeGate()


def run(uri, resource_type, datetime):

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
