'''Implementation of updateMilestoneDetails() API to update project milestones based on project_id.'''
from flask import jsonify, request
from customer_onboarding.database.Customer_Onboarding_db import CustomerOnboarding_db
from customer_onboarding.database.orm_addNewCustomer import OrmMilestones
from flask_restx import Resource
from customer_onboarding.init.helpers import logger
from customer_onboarding.utils.authenticate import user_auth
from customer_onboarding.constants.generals import (PLANNED_DATE, ACTUAL_DATE, STATUS, FETCH)
from customer_onboarding.constants.generals import (PLANNED_DATE, ACTUAL_DATE, STATUS)
from customer_onboarding.constants.messages import (MILESONTE_SUCCESS, MILESONTE_ERROR)

class updateMilestoneDetails(Resource):
    """Update milestones based on project ID."""
    
    @user_auth
    def put(self, project_id):
        with CustomerOnboarding_db() as session:
            row = session.query(OrmMilestones).filter_by(
                project_id=project_id).first()
            if not row:
                logger.info(MILESONTE_ERROR)
                return {STATUS: MILESONTE_ERROR}

            data = request.get_json()
            for each in range(len(data.items())):
                session.query(OrmMilestones).filter(OrmMilestones.project_id == project_id).update(
                    {OrmMilestones.planned_date : data[PLANNED_DATE], OrmMilestones.actual_date: data[ACTUAL_DATE]},
                    synchronize_session=FETCH)
            
            session.commit()
            logger.info(MILESONTE_SUCCESS)

            milestones = session.query(OrmMilestones).filter(OrmMilestones.project_id == project_id)
            milestone_result = jsonify(

                [{

                    PLANNED_DATE: milestone.planned_date,
                    ACTUAL_DATE: milestone.actual_date
                } for milestone in milestones]
            )

            logger.debug(milestone_result)
            return milestone_result