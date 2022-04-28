"""Message constants"""

# connector messages
CONNECTOR = "Customer Onboarding App"
CONNECTOR_INITIALIZING = "Initializing Customer Onboarding App"
CONNECTOR_CONFIG_VERIFICATION = f"Validating {CONNECTOR} configurations"
CONFIG_VERIFICATION_SUCCESS = f"Successfully validated configurations and initialized {CONNECTOR}"
CONNECTOR_STARTED = "Customer Onboarding App has started..."
CONNECTOR_STOPPED = "Shutting Customer Onboarding App"

#Customer Onboarding messages
CUSTOMER_ADD_MSG = "Customer added successfully"
CUSTOMER_ADD_MSG_ERROR = "Customer submission failed"
DATA_INSERTION_ERROR = "data insertion failed"
MILESONTE_SUCCESS = "Milestone updated successfully"
MILESONTE_ERROR = "milestone not found"
NO_PROJECTS_FOUND = 'No projects found for customer with customer_id: {}'
CUSTOMER_DETAILS = "Customer_details: {}"
NO_MILESTONES_FOUND = 'No milestones found for the selected customer'


#Authentication
TOKEN_MISSING = 'token is missing.'
TOKEN_INVALID = 'token is invalid.'
SECRET_KEY = "my_super_secret"