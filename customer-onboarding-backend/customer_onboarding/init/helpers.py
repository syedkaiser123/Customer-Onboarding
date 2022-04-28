"""Initialize configurations and logger for Customer Onboarding App"""
from customer_onboarding.constants.generals import CONFIG, CONFIGURATION_CFG
from customer_onboarding.constants.messages import CONNECTOR
from customer_onboarding.init.connector import init_connector
from customer_onboarding.utils.validators import is_file_exists

# Configurations file path
if not is_file_exists(CONFIG, CONFIGURATION_CFG):
    # Configurations file does not exists.
    raise SystemExit("Configurations file `{name}` does not exists at `{path}`.".format(name=CONFIGURATION_CFG, path=CONFIG))

# Initialise connector and get configurations, logger, and queues for the connector
configs, logger = init_connector(CONNECTOR, CONFIG, CONFIGURATION_CFG)