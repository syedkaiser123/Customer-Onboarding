'''Defining mock functions.'''
import os
import pytest
import requests, json
from flask import jsonify, Flask
from requests.models import Response
from flask_sqlalchemy import SQLAlchemy


def mock_post(*args, **kwargs):
    '''Mock function for post() method'''

    response = Response()
    response.status_code = 200
    response._content = b'{"customer_name": "Splunk","customer_email_id": "support@Splunk.com"}'

    return response

@pytest.fixture
def mock_post_request(*args, **kwargs):
    '''Mock function for post() method'''

    response = Response()
    response.status_code = 200
    response._content = {"customer_name": "Splunk","customer_email_id": "support@Splunk.com"}

    return response

    
def mock_get_request(self):
    '''Mock function for get() method'''
    
    with open("customer_onboarding/database/customer_info.js","r") as f:
        data = json.load(f)
        return data

    
@pytest.fixture
def mock_get():
    '''Mock function for get() method'''
    
    with open("customer_onboarding/database/customer_info.js","r") as f:
        data = json.load(f)
        return data


@pytest.fixture
def mock_flask_app():
    """Fake flask application set up."""

    app_mock = Flask(__name__)
    db = SQLAlchemy(app_mock)
    db.init_app(app_mock)
    return app_mock

@pytest.fixture
def mock_put(*args, **kwargs):
    """creating a mock onject for updateMilestoneDetails put() method."""
    
    response = Response()
    response.status_code = 200
    response._content = {"planned_date": "2023-01-01","actual_date": "2023-01-01"}

    return response._content


@pytest.fixture
def mock_get_sqlalchemy(mocker):
    """sqlaclhemy mock onbject for get() method"""

    mock = mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value = mocker.Mock()
    return mock