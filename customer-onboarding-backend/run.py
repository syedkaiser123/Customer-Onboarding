"""Start the Customer Onboarding App."""
from sac_configurations.context.certify import CertifyConfigurations
from sac_configurations.exceptions.base import ConfigurationsError
from customer_onboarding.constants.generals import (CONFIG, SCHEMA_CONFIG_YAML)
from customer_onboarding.constants.messages import (
    CONFIG_VERIFICATION_SUCCESS, CONNECTOR_CONFIG_VERIFICATION,
    CONNECTOR_INITIALIZING, CONNECTOR_STARTED, CONNECTOR_STOPPED)
from customer_onboarding.init.configurations import get_schema_definition
from customer_onboarding.init.helpers import configs, logger
from customer_onboarding.app import create_app



if __name__ == "__main__":
    """Start Customer Onboarding App.
    1. Read the schema definitions.
    2. Verify the configurations and assign default values.
    """
    
    logger.info(CONNECTOR_INITIALIZING)
    # Validate all the configurations
    try:
        logger.info(CONNECTOR_CONFIG_VERIFICATION)
        # Get Schema
        schema = get_schema_definition(CONFIG, SCHEMA_CONFIG_YAML)
        # Certify the configurations
        certify = CertifyConfigurations(schema)
        certify.verify_n_assign_default(configs)
        logger.info(CONFIG_VERIFICATION_SUCCESS)
    except (ConfigurationsError) as err:
        logger.error(str(err))
    else:
        try:
            create_app().run(debug=True)
            logger.info(CONNECTOR_STARTED)
        except KeyboardInterrupt:
            logger.info(CONNECTOR_STOPPED)



