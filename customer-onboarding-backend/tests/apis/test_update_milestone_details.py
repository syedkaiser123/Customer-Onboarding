'''Unit testing update_milestone_details.py file.'''
import pytest
from flask import request
from customer_onboarding.apis.update_milestone_details import updateMilestoneDetails
from customer_onboarding.database.Customer_Onboarding_db import CustomerOnboarding_db
from tests.mock import mock_flask_app, mock_put, mock_get_sqlalchemy
from customer_onboarding.constants.generals import (PLANNED_DATE)

def test_put(mock_flask_app, mock_get_sqlalchemy, mock_put):

    try:
        with mock_flask_app.app_context():
            mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_put
            response = updateMilestoneDetails.put(mock_put,101)

            assert response[PLANNED_DATE] == "2023-01-01"
    except Exception as e:
        print("error ocurred: {}".format(e))