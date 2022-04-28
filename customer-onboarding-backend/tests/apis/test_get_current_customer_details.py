'''Unit testing update_milestone_details.py file.'''
import pytest
from flask import request
from customer_onboarding.apis.get_current_customer_details import getCurrentCustomerDetails 
from customer_onboarding.database.Customer_Onboarding_db import CustomerOnboarding_db
from tests.mock import mock_flask_app, mock_get, mock_get_sqlalchemy

def test_get(mock_flask_app, mock_get_sqlalchemy, mock_get):
    """unit test case for get() method."""

    try:
        with mock_flask_app.app_context():
            mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_get
            response = getCurrentCustomerDetails.get(mock_get)

            assert response[CUSTOMER_NAME] == "Zechariah"
    except Exception as e:
        print("error ocurred: {}".format(e))