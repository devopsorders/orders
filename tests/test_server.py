"""
Order API Service Test Suite
Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import logging
import os
import unittest

from flask_api import status  # HTTP Status Codes

# from .order_factory import OrderFactory
import app.service as service
# from unittest.mock import MagicMock, patch
from app.models import db

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')


######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrderServer(unittest.TestCase):
    """ Order Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        service.app.debug = False
        service.initialize_logging(logging.INFO)
        # Set up the test database
        service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        service.init_db()
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def _create_orders(self, count):
    #     """ Factory method to create orders in bulk """
    #     orders = []
    #     for _ in range(count):
    #         test_order = OrderFactory()
    #         resp = self.app.post('/orders',
    #                              json=test_order.serialize(),
    #                              content_type='application/json')
    #         self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test order')
    #         new_order = resp.get_json()
    #         test_order.id = new_order['id']
    #         orders.append(test_order)
    #     return orders

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'Orders REST API Service')

    # TODO add rest of tests here


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
