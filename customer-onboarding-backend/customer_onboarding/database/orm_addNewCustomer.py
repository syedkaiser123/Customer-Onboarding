"""ORM to query database table 'customer' for the required fields."""
from customer_onboarding.database.Customer_Onboarding_db import db
from customer_onboarding.constants.generals import CUSTOMER
from customer_onboarding.constants.generals import (CUSTOMER, MILESTONES, PROJECT)

class OrmCustomer(db.Model):
    """To query and fetch data from these fields."""

    __tablename__ = CUSTOMER
    __table_args__ = {"extend_existing": True}
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), unique=True, nullable=False)
    customer_email_id = db.Column(db.String(100), unique=True, nullable=False)


    # fmt: off
    def __init__(self,customer_name,customer_email_id):
        """Init function for Customer class."""

        self.customer_name = customer_name
        self.customer_email_id = customer_email_id
        self.customer_email_id = customer_email_id


class OrmProject(db.Model):
    """To query and fetch data from these fields."""

    __tablename__ = PROJECT
    __table_args__ = {"extend_existing": True}
    project_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    customer_id = db.Column(db.Integer, primary_key=False)
    project_name = db.Column(db.String(50), unique=True, nullable=False)


    def __init__(self,customer_id,project_name):

        self.customer_id = customer_id
        self.project_name = project_name



class OrmMilestones(db.Model):
    """To query and fetch data from these fields."""

    __tablename__ = MILESTONES
    __table_args__ = {"extend_existing": True}
    project_id = db.Column(db.Integer, primary_key=False)
    milestone_name = db.Column(db.String(100), unique=True, nullable=False)
    sow_date = db.Column(db.Date, unique=True, nullable=False, primary_key=True)
    planned_date = db.Column(db.Date, unique=True, nullable=False)
    actual_date = db.Column(db.Date, unique=True, nullable=False)


    # fmt: off
    def __init__(self,project_id,milestone_name,sow_date,planned_date,actual_date):
        """Init function for Milestones class."""
        
        self.project_id = project_id
        self.milestone_name = milestone_name
        self.sow_date = sow_date
        self.planned_date = planned_date
        self.actual_date = actual_date
