"""
Test cases for Order Model
Test cases can be run with:
  nosetests
  coverage report -m
"""

import os
import unittest

from app import app
from app.models import Order, OrderItem, DataValidationError, db
from app.models import STATUS_RECEIVED

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')


######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrders(unittest.TestCase):
    """ Test Cases for Orders """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Order.init_db(app)
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_serialize_an_order(self):
        """ Test serialization of an order """
        order_items = [{'product_id': 1,
                        'name': 'Protein Bar (12 Count)',
                        'quantity': 3,
                        'price': 18.45,
                        },
                       {'product_id': 2,
                        'name': 'AirPods',
                        'quantity': 1,
                        'price': 159,
                        }]
        order = Order(customer_id=1, status=STATUS_RECEIVED)
        for order_item in order_items:
            order.order_items.append(OrderItem(product_id=order_item['product_id'],
                                               name=order_item['name'],
                                               quantity=order_item['quantity'],
                                               price=order_item['price']))

        data = order.serialize()
        self.assertIsNotNone(data)
        self.assertIn('id', data)
        self.assertIsNone(data['id'])
        self.assertIn('order_items', data)
        self.assertEqual(data['order_items'][0]['name'], 'Protein Bar (12 Count)')
        self.assertEqual(data['order_items'][0]['quantity'], 3)
        self.assertEqual(data['order_items'][0]['price'], 18.45)

        self.assertEqual(data['order_items'][1]['name'], 'AirPods')
        self.assertEqual(data['order_items'][1]['quantity'], 1)
        self.assertIn('customer_id', data)
        self.assertEqual(data['customer_id'], 1)

    def test_deserialize_an_order(self):
        """ Test deserialization of an order """
        order_items = [{'product_id': 1,
                        'name': 'Protein Bar (12 Count)',
                        'quantity': 3,
                        'price': 18.45,
                        },
                       {'product_id': 2,
                        'name': 'AirPods',
                        'quantity': 1,
                        'price': 159,
                        }]
        data = {'customer_id': 1, 'status': STATUS_RECEIVED, 'order_items': order_items}
        order = Order()
        order.deserialize(data)
        self.assertIsNotNone(order)
        self.assertIsNone(order.id)
        self.assertEqual(order.order_items[0].quantity, 3)
        self.assertEqual(order.order_items[0].total, 55.35)
        self.assertEqual(order.customer_id, 1)
        self.assertEqual(order.order_items[1].name, 'AirPods')
        self.assertEqual(order.order_items[1].price, 159)
        self.assertEqual(order.total, 214.35)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is a string"
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
