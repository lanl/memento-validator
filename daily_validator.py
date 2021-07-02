import json
import xml.etree.ElementTree as ElementTree
from typing import Union

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
    archive_list_path: str = "config.xml"

    tree = ElementTree.parse(archive_list_path)
    root = tree.getroot()
    t = TimeGate()

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
                # TODO : Add code for testing (pass as **test_params)
                validator = _get_validator(resource_type)
                if validator is None:
                    print("Invalid resource type")
                else:
                    reports = validator.validate(**test_params)
                    json.dump({
                        "type": resource_type,
                        "params": test_params,
                        "pipeline": validator.name(),
                        "results": [report.to_json() for report in reports]
                    }, output_file, ensure_ascii=False, indent=4)
            output_file.close()
