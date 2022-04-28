"""Flask app init file for Customer Onboarding module."""
from flask import Flask
from flask_restx import Api
from customer_onboarding.database.Customer_Onboarding_db import db
from customer_onboarding.init.helpers import logger
from customer_onboarding.apis.add_new_customer import addNewCustomer
from customer_onboarding.constants.default import JWT_SECRET_KEY
from customer_onboarding.constants.generals import (JSON_SORT_KEYS, SQLALCHEMY_TRACK_MODIFICATIONS,
                                                    VERSION, CUSTOMER_ONBOARDING, DESCRIPTION1, DESCRIPTION2,
                                                    ADD_CUSTOMER_API_ENDPOINT, API)

from customer_onboarding.apis.get_customer_projects import getCustomerProjects
from customer_onboarding.apis.update_milestone_details import updateMilestoneDetails
from customer_onboarding.constants.generals import (JSON_SORT_KEYS, SQLALCHEMY_TRACK_MODIFICATIONS, GET_CUSTOMER_API_ENDPOINT,
                                                    VERSION, CUSTOMER_ONBOARDING, DESCRIPTION1, DESCRIPTION2,
                                                    CUSTOMER_API_ENDPOINT, PROJECT_API_ENDPOINT, API, MILESTONE_API_ENDPOINT)
from customer_onboarding.apis.get_current_customer_details import getCurrentCustomerDetails



def create_app():
    """
    To create app.
    connect to db,
    register apis to verious endpoints,
    return the app.
    """

    app = Flask(__name__)
    app.config[JSON_SORT_KEYS] = False
    app.config[SQLALCHEMY_TRACK_MODIFICATIONS] = False
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    db.app = app
    db.init_app(app)
    api = Api(app, version=VERSION, title=CUSTOMER_ONBOARDING,
              description=DESCRIPTION1)

    customer_onboarding = api.namespace(
        API, description=DESCRIPTION2)

    customer_onboarding.add_resource(addNewCustomer, CUSTOMER_API_ENDPOINT)
    customer_onboarding.add_resource(getCustomerProjects, PROJECT_API_ENDPOINT)
    customer_onboarding.add_resource(updateMilestoneDetails, MILESTONE_API_ENDPOINT)
    customer_onboarding.add_resource(getCurrentCustomerDetails, GET_CUSTOMER_API_ENDPOINT)

    logger.debug(app)
    return app