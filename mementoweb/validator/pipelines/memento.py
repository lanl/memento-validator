from typing import List

from mementoweb.validator.pipelines import DefaultPipeline
from mementoweb.validator.tests.test import TestSetting
from mementoweb.validator.tests.uri_test import URITest


class Memento(DefaultPipeline):

    # TODO : Add memento tests
    _tests: List[TestSetting] = [
        {'test': URITest(), 'params': None}
    ]
