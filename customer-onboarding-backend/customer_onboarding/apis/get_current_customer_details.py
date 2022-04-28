"""Implementation of getCurrentCustomerDetails() API endpoint."""
from flask import jsonify
from datetime import date
from flask_restx import Resource
from customer_onboarding.init.helpers import logger
import itertools
import operator
from customer_onboarding.database.Customer_Onboarding_db import CustomerOnboarding_db, db
from customer_onboarding.utils.authenticate import user_auth
from customer_onboarding.database.orm_addNewCustomer import OrmCustomer, OrmProject, OrmMilestones
from customer_onboarding.constants.generals import (CUSTOMER_ID, CUSTOMER_NAME, CUSTOMER_EMAIL_ID,
                                                    SOW_DATE, PLANNED_DATE, ACTUAL_DATE, PROJECT_ID,
                                                    ERROR, EXCEPTION)
from customer_onboarding.constants.messages import (CUSTOMER_DETAILS, NO_MILESTONES_FOUND)


class getCurrentCustomerDetails(Resource):
    
    @user_auth
    def get(self):
        """Fetch current customer details from the 'customer' table based on the sow_date and planned_date."""

        milestones = CustomerOnboarding_db().query(OrmMilestones).filter(OrmMilestones.project_id == OrmProject.project_id and OrmProject.customer_id == OrmCustomer.customer_id).filter(OrmMilestones.sow_date <= date.today()).filter(OrmMilestones.planned_date >= date.today())
        customer_details = []
        try:
            if milestones.count():
                for milestone in milestones:
                    project = CustomerOnboarding_db().query(OrmProject).filter(OrmProject.project_id == milestone.project_id)[0]
                    customer = CustomerOnboarding_db().query(OrmCustomer).filter(OrmCustomer.customer_id == project.customer_id)[0]

                    customer_details.append(
                        {
                                CUSTOMER_ID: customer.customer_id,
                                CUSTOMER_NAME: customer.customer_name,
                                CUSTOMER_EMAIL_ID: customer.customer_email_id
                        }
                    )

            logger.debug(CUSTOMER_DETAILS.format(customer_details))
            return jsonify(sorted(customer_details, key=operator.itemgetter(CUSTOMER_ID)))

        except Exception as e:
            return ({ERROR: NO_MILESTONES_FOUND, EXCEPTION:'{}'.format(e)})

        except TypeError as e:
            raise TypeError({ERROR: '{}'.format(e)})