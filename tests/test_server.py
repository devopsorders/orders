"""
Order API Service Test Suite
Test cases can be run with the following:
  pytest
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import json
import logging
import unittest
from datetime import datetime, date, timedelta
from unittest.mock import patch

from flask_api import status  # HTTP Status Codes

import app.service as service
from app.models import Order, OrderItem, db, OrderStatus
from .order_factory import OrderFactory


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
        # service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

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

    def _create_orders(self, count):
        """ Factory method to create orders in bulk """
        orders = []
        for _ in range(count):
            test_order = OrderFactory()
            resp = self.app.post('/orders',
                                 json=test_order.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test order')
            new_order = resp.get_json()
            test_order.id = new_order['id']
            orders.append(test_order)
        return orders

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # data = resp.data
        # self.assertIn('<title>Order REST API Service</title>', data)

    def test_get_order(self):
        """ Get a single order """
        # get the id of an order
        test_order = self._create_orders(1)[0]
        resp = self.app.get('/orders/{}'.format(test_order.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['id'], test_order.id)

    def test_get_order_not_found(self):
        """ Get an order that is not found """
        resp = self.app.get('/orders/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_order(self):
        """ Create a new Order """
        test_order_item = OrderItem(product_id=1, name='Test Item', quantity=10, price=69.00)
        test_order = Order(customer_id=1, status=OrderStatus.RECEIVED, order_items=[test_order_item])
        resp = self.app.post('/orders',
                             json=test_order.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set

        location = resp.headers.get('Location', None)
        self.assertTrue(location is not None)

        # Check the data is correct
        new_order = resp.get_json()
        self.assertTrue(new_order['id'] is not None, "No order ID")
        self.assertEqual(new_order['status'], test_order.status, "Status does not match")
        self.assertEqual(new_order['customer_id'], test_order.customer_id, "Customer ID does not match")
        self.assertEqual(new_order['order_items'][0]['quantity'], test_order.order_items[0].quantity,
                         "Quantity does not match")

        # Check that the location header was correct
        resp = self.app.get(location,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_order = resp.get_json()
        self.assertEqual(new_order['status'], test_order.status, "Status do not match")
        self.assertEqual(new_order['customer_id'], test_order.customer_id, "Customer Id does not match")
        self.assertEqual(len(new_order['order_items']), len(test_order.order_items.all()), "Order items don't match")

    def test_update_order(self):
        """ Update an existing Order """
        # create a order to update
        test_order = OrderFactory()
        resp = self.app.post('/orders',
                             json=test_order.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = resp.get_json()
        new_order['status'] = OrderStatus.SHIPPED
        resp = self.app.put('/orders/{}'.format(new_order['id']),
                            json=new_order,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_order = resp.get_json()
        self.assertEqual(updated_order['status'], OrderStatus.SHIPPED)

    def test_update_order_not_found(self):
        """ Update an order that is not found """
        test_order = OrderFactory()
        resp = self.app.put('/orders/0',
                            json=test_order.serialize(),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        """ Delete an order"""
        test_order = self._create_orders(1)[0]
        resp = self.app.delete('/orders/{}'.format(test_order.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/orders/{}'.format(test_order.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_orders(self):
        """ Delete all orders and reset auto increment counter"""
        self._create_orders(10)
        resp = self.app.delete('/orders/reset',
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # make sure they are deleted
        resp = self.app.get('/orders',
                            content_type='application/json')
        data = resp.get_json()
        self.assertEqual(len(data), 0)

    def test_get_order_list(self):
        """ Get a list of Orders """
        self._create_orders(5)
        resp = self.app.get('/orders')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_query_order_list_by_status(self):
        """ Query Orders by Order Status """
        orders = self._create_orders(10)
        test_status = orders[0].status
        status_orders = [order for order in orders if order.status == test_status]
        resp = self.app.get('/orders',
                            query_string='status={}'.format(test_status))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(status_orders))
        # check the data just to be sure
        for order in data:
            self.assertEqual(order['status'], test_status)

    def test_query_order_list_by_since_date(self):
        """ Query Orders by Order Since a Date """
        self._create_orders(5)

        # add old order
        test_order = OrderFactory()
        test_order.order_date = datetime.today() - timedelta(days=300)
        resp = self.app.post('/orders',
                             json=test_order.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create old test order')

        resp = self.app.get('/orders')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        orders_since = date.today() - timedelta(days=30)
        resp = self.app.get('/orders',
                            query_string='orders_since={}'.format(orders_since.strftime('%Y-%m-%d')))

        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_cancel_order(self):
        """ Cancel a single Order """
        test_order = self._create_orders(1)[0]
        resp = self.app.put('/orders/{}/cancel'.format(test_order.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        cancelled_order = resp.get_json()
        self.assertEqual(cancelled_order['status'], OrderStatus.CANCELED)

    def test_cancel_non_existing_order(self):
        """ Cancel an order that doesn't exist """
        resp = self.app.put('/orders/0/cancel', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_content_type(self):
        test_order_item = OrderItem(product_id=1, name="Test Item", quantity=10, price=69.00)
        test_order = Order(customer_id=1, status=OrderStatus.RECEIVED, order_items=[test_order_item])
        resp = self.app.post('/orders',
                             json=test_order.serialize(),
                             content_type='application/xml')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_bad_request(self):
        """ Test a Bad Request by posting invalid Order json """
        # bad order with no customer id
        bad_order = dict(status=OrderStatus.RECEIVED)
        data = json.dumps(bad_order)
        resp = self.app.post('/orders',
                             json=data,
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed(self):
        """ Test a sending invalid http method """
        resp = self.app.post('/orders/1')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('app.service.Order.all')
    def test_unexpected_error(self, bad_request_mock):
        """ Test an unexpected error from Find All """
        bad_request_mock.side_effect = KeyError
        resp = self.app.get('/orders')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
