"""Unit testing orm_addNewCustomer API."""
import pytest
from customer_onboarding.database.orm_addNewCustomer import OrmCustomer
from customer_onboarding.database.orm_addNewCustomer import OrmMilestones
from customer_onboarding.database.orm_addNewCustomer import OrmProject
projects = OrmProject("customer_id","project_name")
milestones = OrmMilestones("project_id","milestone_name","sow_date","planned_date","actual_date")
customer = OrmCustomer("customer_name","customer_email_id")

def test_ormCustomer():
    '''unit test case for class Customer.'''
    
    assert customer.__tablename__ == "customer"


def test_OrmMilestones():
    '''unit test case for class Milestones.'''
    
    assert milestones.__tablename__ == "milestones"


def test_OrmProject(self):
    '''unit test case for class Project.'''
    
    assert projects.__tablename__ == "project"
