"""Initialise the configurations for Customer Onboarding"""
import os
from typing import Any, Dict, List
from sac_configurations.context.schema import Schema
from sac_configurations.input.cfg import CFGConfig


def get_schema_definition(schema_dir: str, filename: str) -> Schema:
    """Get schema definition
    :param schema_dir: Schema file directory
    :type schema_dir: str
    :param filename: Schema filename
    :type filename: str
    :return: Schema definition
    :rtype: Schema
    """
    filepath = os.path.join(schema_dir, filename)
    return Schema(filepath)


def read_configurations(filenames: List[str]) -> Dict[str, Any]:
    """Read configurations from the configuraiton files
    :param filenames: List of configurations files
    :type filenames: List[str]
    :return: Configurations read from the list of configurations files
    :rtype: Dict[str, Any]
    """
    config = CFGConfig()
    config.read(filenames)
    return config.to_dict()


def get_configurations(config_dir: str, filename: str) -> Dict[str, Any]:
    """Get configurations privided in configurations files
    :param config_dir: Configurations file directory
    :type config_dir: str
    :param filename: Configurations file name
    :type filename: str
    :return: Configuraitons read from configurations files
    :rtype: Dict[str, Any]
    """
    filepath = os.path.join(config_dir, filename)
    
    return read_configurations([filepath])