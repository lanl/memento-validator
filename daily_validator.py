import xml.etree.ElementTree as ElementTree
from mementoweb.validator.pipelines.timegate import TimeGate

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
            for test_info in test_info_nodes:
                resource_type = test_info.attrib.pop("type")
                test_params = test_info.attrib
                # TODO : Add code for testing (pass as **test_params)
                print(resource_type + " : " + str(test_params))
