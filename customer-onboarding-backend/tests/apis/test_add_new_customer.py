"""Unit testing addNewCustomer API."""
import pytest
from flask import request, jsonify
from tests.mock import mock_post, mock_post_request, mock_flask_app, mock_get_sqlalchemy
from customer_onboarding.apis.add_new_customer import addNewCustomer

ADD_NEW_CUSTOMER = "customer_onboarding.apis.add_new_customer.addNewCustomer.post"

def test_post_request(mocker):
    """unit test case for post() method with success response."""

    mocker.patch(ADD_NEW_CUSTOMER, mock_post)

    request = addNewCustomer.post()
    assert request._content == b'{"customer_name": "Splunk","customer_email_id": "support@Splunk.com"}'


def test_post(mock_flask_app, mock_get_sqlalchemy, mock_post_request):
    """unit test case for post() method with success response."""
    try:
        with mock_flask_app.app_context():
            mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_post_request
            response = addNewCustomer.post(mock_post_request)

            assert response["customer_name"] == "Splunk"
            assert response["customer_email_id"] == "support@Splunk.com"
    except Exception as e:
        print("error ocurred: {}".format(e))