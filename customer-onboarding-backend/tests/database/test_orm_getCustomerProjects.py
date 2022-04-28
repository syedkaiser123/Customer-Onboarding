'''Unit testing orm_getCustomerProjects.py file.'''
import pytest
from customer_onboarding.database.orm_getCustomerProjects import OrmProject
projects = OrmProject("project_name")

def test_OrmProject():
    '''unit test case for class Project.'''
    
    assert projects.__tablename__ == "project"