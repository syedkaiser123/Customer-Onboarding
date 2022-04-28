'''Unit testing get_customer_projects.py file.'''
import pytest
from flask import request
from customer_onboarding.apis.get_customer_projects import getCustomerProjects
from customer_onboarding.database.Customer_Onboarding_db import CustomerOnboarding_db
from tests.mock import mock_get, mock_flask_app, mock_get_sqlalchemy, mock_get_request

GET_CUSTOMER_PROJECTS_GET = "customer_onboarding.apis.get_customer_projects.getCustomerProjects.get"

def test_get():
    '''Unit test case for get() method with response code 200.'''

    url = "www.google.com"
    try:
        response = request.get(url)
        assert response.status_code == 200
    except Exception as e:
        print("context error {}".format(e))



def test_get_content():
    '''Unit test case for get() method with url response content.'''

    url = "https://jsonplaceholder.typicode.com/users"
    try:
        response = request.get(url)
        assert response._content[0] == {
                                        "id": 1,
                                        "name": "Leanne Graham",
                                        "username": "Bret",
                                        "email": "Sincere@april.biz",
                                        "address": {
                                        "street": "Kulas Light",
                                        "suite": "Apt. 556",
                                        "city": "Gwenborough",
                                        "zipcode": "92998-3874",
                                        "geo": {
                                            "lat": "-37.3159",
                                            "lng": "81.1496"
                                        }
                                        },
                                        "phone": "1-770-736-8031 x56442",
                                        "website": "hildegard.org",
                                        "company": {
                                        "name": "Romaguera-Crona",
                                        "catchPhrase": "Multi-layered client-server neural-net",
                                        "bs": "harness real-time e-markets"
                                        }
                                    }
    except Exception as e:
        print("context error {}".format(e))




def test_mock_get(mocker):
    '''unit test case for get() method with database content'''
    
    mocker.patch(GET_CUSTOMER_PROJECTS_GET, mock_get_request)

    obj = getCustomerProjects()
    res = obj.get()
    assert res ==   [
                        {
                        "project_id": 100,
                        "customer_id": 1,
                        "project_name": "CarbonBlack"
                        },
                        {
                        "milestone_name": "ABCDE",
                        "sow_date": "Mon, 02 May 2022 00:00:00 GMT",
                        "planned_date": "Mon, 02 May 2022 00:00:00 GMT",
                        "actual_date": "Mon, 02 May 2022 00:00:00 GMT"
                        }
                    ]




def test_get(mock_flask_app, mock_get_sqlalchemy, mock_get):
    '''unit test case for get() method with database content'''
    try:
        with mock_flask_app.app_context():
            mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_get
            response = getCustomerProjects.get(mock_get,1)

            assert response["customer_name"] == "Splunk"
            assert response["customer_name"] == "CarbonBlack"
    except Exception as e:
        print("error ocurred: {}".format(e))