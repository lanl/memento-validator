from typing import List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


class Config:
    """
    Provides access to the configuration parameters from config.xml.

    The configuration only supports xml.

    """

    _root: ElementTree = None

    file_path = "config.xml"

    @staticmethod
    def get_env(xpath: str) -> List[Element]:
        """
        Get specified configuration parameter from "config.xml" using the specified xpath.
        :param xpath: xpath of the element
        :return: list of matching elements in document order
        """
        if Config._root is None:
            Config._read()

        return Config._root.findall(xpath)

    @staticmethod
    def _read():
        Config._root = ElementTree.parse(Config.file_path).getroot()
