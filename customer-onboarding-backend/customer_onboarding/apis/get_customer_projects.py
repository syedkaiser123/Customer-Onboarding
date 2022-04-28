'''getCustomerProject() API to fetch customer projects from the database.'''
from flask import jsonify
from customer_onboarding.database.Customer_Onboarding_db import CustomerOnboarding_db
from customer_onboarding.database.orm_addNewCustomer import OrmProject, OrmMilestones
from customer_onboarding.utils.authenticate import user_auth
from customer_onboarding.constants.generals import (PROJECT_ID, PROJECT_NAME, ERROR,
                                                    CUSTOMER_ID, MILESTONE_NAME, SOW_DATE,
                                                    PLANNED_DATE, ACTUAL_DATE, EXCEPTION)
from customer_onboarding.constants.messages import (NO_PROJECTS_FOUND)
from customer_onboarding.database.orm_addNewCustomer import OrmProject, OrmMilestones
from customer_onboarding.database.orm_addNewCustomer import OrmProject, OrmCustomer, OrmMilestones
from customer_onboarding.constants.generals import (PROJECT_ID, PROJECT_NAME,
                                                    CUSTOMER_ID, MILESTONE_NAME, SOW_DATE,
                                                    PLANNED_DATE, ACTUAL_DATE)
from flask_restx import Resource
from customer_onboarding.init.helpers import logger
import itertools
import operator

class getCustomerProjects(Resource):
    @user_auth
    def get(self,cust_id):
        """Query db table 'project' and 'milestones' to return these fields
        :project_id
        :customer_id
        :project_name
        :milestone_name
        :sow_date
        :planned_date
        :actual_date
        """

        #fetch projects based on the customer_id
        try:
            projects = CustomerOnboarding_db().query(OrmProject).filter(OrmProject.customer_id == cust_id)
            logger.debug(projects)
            project_result = [
                {
                    PROJECT_ID: project.project_id,
                    CUSTOMER_ID: project.customer_id,
                    PROJECT_NAME: project.project_name,

                }for project in projects
            ]

            
            project_id = project_result[0][PROJECT_ID]

            project_result = sorted((project_result), key=operator.itemgetter(CUSTOMER_ID))

            projects_list = []
            for i, g in itertools.groupby(project_result, key=operator.itemgetter(CUSTOMER_ID)):
                projects_list.append(list(g))
            logger.debug(projects_list)

            #fetch milestones based on the project_id
            milestones = CustomerOnboarding_db().query(OrmMilestones).filter(OrmMilestones.project_id == project_id)
            logger.debug(milestones)
            milestones_result = [
                {
                    MILESTONE_NAME: milestone.milestone_name,
                    SOW_DATE: milestone.sow_date,
                    PLANNED_DATE: milestone.planned_date,
                    ACTUAL_DATE: milestone.actual_date

                }for milestone in milestones
            ]

            milestones_result = sorted((milestones_result), key=operator.itemgetter(MILESTONE_NAME))

            milestones_list = []
            for i, g in itertools.groupby(milestones_result, key=operator.itemgetter(MILESTONE_NAME)):
                milestones_list.append(list(g))
            logger.debug(milestones_list)

            return jsonify(projects_list, milestones_list)
        
        except Exception as e:
            return (
                    {ERROR:NO_PROJECTS_FOUND.format(cust_id),
                    EXCEPTION:'{}'.format(e)}
                    )