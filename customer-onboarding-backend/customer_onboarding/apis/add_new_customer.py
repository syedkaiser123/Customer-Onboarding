'''addNewCustomer() API to post/add new customer into the database.'''
from flask import jsonify, request
from customer_onboarding.database.orm_addNewCustomer import OrmCustomer
import json
from customer_onboarding.database.orm_addNewCustomer import OrmCustomer, OrmProject, OrmMilestones
from customer_onboarding.database.Customer_Onboarding_db import CustomerOnboarding_db
from flask_restx import Resource
from customer_onboarding.init.helpers import logger
from customer_onboarding.utils.authenticate import user_auth
from customer_onboarding.constants.generals import (CUSTOMER_ID, CUSTOMER_NAME, CUSTOMER_EMAIL_ID,STATUS, ERROR,
                                                    STATUS, ERROR, PROJECT_ID, PROJECT_NAME, MILESTONE_NAME,
                                                    SOW_DATE, PLANNED_DATE, ACTUAL_DATE)
from customer_onboarding.constants.messages import (CUSTOMER_ADD_MSG, CUSTOMER_ADD_MSG_ERROR,
                                                    DATA_INSERTION_ERROR)


class addNewCustomer(Resource):
    @user_auth
    def post(self):
        """Post data to customer table."""
        data = request.get_json()
        new_customer = OrmCustomer(
            customer_name = data[CUSTOMER_NAME],
            customer_email_id = data[CUSTOMER_EMAIL_ID])


        try:
            with CustomerOnboarding_db() as session:
                session.add(new_customer)
                session.commit()
                OnboardingCustomers = session.query(OrmCustomer).all()
                new_project = OrmProject(customer_id = new_customer.customer_id,project_name = data[PROJECT_NAME])

                session.add(new_project)
                session.commit()


                new_milestones = OrmMilestones(
                    project_id = new_project.project_id,
                    milestone_name = data[MILESTONE_NAME],
                    sow_date = data[SOW_DATE],
                    planned_date = data[PLANNED_DATE],
                    actual_date = data[ACTUAL_DATE]
                    )

                session.add(new_milestones)
                session.commit()
                OnboardingCustomers = session.query(OrmCustomer).filter(OrmCustomer.customer_id == new_customer.customer_id)
                customer_info = [
                        {
                            CUSTOMER_ID: customer.customer_id,
                            CUSTOMER_NAME: customer.customer_name,
                            CUSTOMER_EMAIL_ID: customer.customer_email_id,
                            PROJECT_ID: new_project.project_id,
                            PROJECT_NAME: new_project.project_name,

                        }
                        for customer in OnboardingCustomers
                    ]
                
                milestone_details = session.query(OrmMilestones).filter(OrmMilestones.project_id == new_project.project_id)
                customer_milestones = [{

                            MILESTONE_NAME: milestone.milestone_name,
                            SOW_DATE: milestone.sow_date,
                            PLANNED_DATE: milestone.planned_date,
                            ACTUAL_DATE: milestone.actual_date

                }for milestone in milestone_details]
                
                logger.info(CUSTOMER_ADD_MSG)
                                
                customer_info.extend(customer_milestones)
                logger.debug(customer_info)
            return (jsonify(customer_info))


        except Exception as e:
            logger.info(CUSTOMER_ADD_MSG_ERROR)
            return {STATUS: DATA_INSERTION_ERROR, ERROR: str(e)}