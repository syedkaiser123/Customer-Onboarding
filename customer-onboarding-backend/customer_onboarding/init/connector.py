"""Initialize Customer Onboarding App."""
from logging import Logger
from typing import Any, Dict, Tuple
from sac_log import logger as sac_logger
from sac_log.exceptions import LoggingError
from customer_onboarding.constants.generals import LOGGING
from customer_onboarding.init.configurations import get_configurations


def init_connector(name: str, config_dir: str, config_file: str) -> Tuple[Dict[str, Any], Logger, Any]:
    """Initialise te connector.

    This initialises objects required for connector to work as follows:

    1. configurations
    2. logger

    :param name: Name of the connector
    :type name: str
    :param config_dir: Configurations directory
    :type config_dir: str
    :param config_file: Configurations filename
    :type config_file: str
    :raises SystemExit: If the error occured while creating a logger
    :return: Connector configurations, logger
    """
    # Get configurations
    configs = get_configurations(config_dir, config_file)

    # Get logger instance
    try:
        logger = sac_logger.get_logger(name, configs[LOGGING])
    except LoggingError as err:
        raise SystemExit(str(err)) from err


    return configs, logger
