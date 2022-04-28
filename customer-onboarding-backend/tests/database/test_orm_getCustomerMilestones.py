'''Unit testing orm_getCustomerMilestones.py file.'''
import pytest
from customer_onboarding.database.orm_getCustomerMilestones import OrmMilestones
milestones = OrmMilestones("milestone_name","sow_date","planned_date","actual_date")

def test_OrmMilestones():
    '''unit test case for class Milestones.'''
    
    assert milestones.__tablename__ == "milestones"