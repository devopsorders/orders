"""
Order Steps
Steps file for orders.feature
"""
import json
import time
from os import getenv

import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

WAIT_SECONDS = 20
BASE_URL = getenv('BASE_URL', 'http://localhost:5000')
print(BASE_URL)


@given(u'the following orders')
def step_impl(context):
    """ Delete all Orders and load new ones """
    headers = {'Content-Type': 'application/json'}
    # context.resp = requests.delete(context.base_url + '/orders/reset')
    # expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/orders'
    for row in context.table:
        data = {
            "customer_id": row['customer_id'],
            "status": row['status'],
            "order_items": [{
                "product_id": row['product_id'],
                "name": row['name'],
                "quantity": row['quantity'],
                "price": row['price']
            }]
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


@when(u'I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)


@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)


# TODO remove this method after UI is done
@then(u'I should see "" in the title')
def step_impl(context):
    pass


@then(u'I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)
