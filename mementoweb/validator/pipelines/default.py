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

from typing import List

from mementoweb.validator.tests.test import TestReport


class PipelineResult:
    reports: List[TestReport]

    timemaps: List[str]

    timegates: List[str]

    mementos: List[str]

    def __init__(self):
        self.reports = []
        self.timemaps = []
        self.timegates = []
        self.mementos = []

    def to_json(self):
        return {
            "timemaps": self.timemaps,
            "timegates": self.timegates,
            "reports": [report.to_json() for report in self.reports]
        }


class DefaultPipeline:

    result: PipelineResult

    def __init__(self):
        self.result = PipelineResult()

    def name(self) -> str:
        return self.__module__ + '.' + self.__class__.__name__

    def validate(self,
                 uri: str,
                 datetime='Thu, 10 Oct 2009 12:00:00 GMT',
                 accept=''
                 ) -> PipelineResult:
        pass
