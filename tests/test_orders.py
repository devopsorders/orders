"""
Test cases for Order Model
Test cases can be run with:
  pytest
  coverage report -m
"""

import unittest
from datetime import datetime, date, timedelta

from app import app
from app.models import Order, OrderItem, OrderStatus, DataValidationError, db


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
        # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

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

    def test_delete_all(self):
        order_item = OrderItem(product_id=1, name="Protein Bar (12 Count)", quantity=3, price=69.00)
        order = Order(customer_id=1, status=OrderStatus.RECEIVED, order_items=[order_item])
        order.save()
        order.delete_all()
        self.assertEqual(len(order.all()), 0)

    def test_create_an_order(self):
        """ Create an order with an item and assert that it exists """
        order_item = OrderItem(product_id=1, name="Protein Bar (12 Count)", quantity=3, price=69.00)
        order = Order(customer_id=1, status=OrderStatus.RECEIVED, order_items=[order_item])
        self.assertTrue(order is not None)
        self.assertEqual(order.id, None)
        self.assertEqual(order.status, OrderStatus.RECEIVED)
        self.assertEqual(order.order_items[0].quantity, 3)

    def test_add_an_order(self):
        """ Create an order with an item and add it to the database """
        orders = Order.all()
        self.assertEqual(orders, [])
        order_item = OrderItem(product_id=1, name="Protein Bar (12 Count)", quantity=3, price=69.00)
        order = Order(customer_id=1, status=OrderStatus.RECEIVED, order_items=[order_item])
        self.assertTrue(order is not None)
        self.assertEqual(order.id, None)
        order.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(order.id, 1)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_update_an_order(self):
        """ Update an Order """
        order_item = OrderItem(product_id=1, name="Protein Bar (12 Count)", quantity=3, price=69.00)
        order = Order(customer_id=1, status=OrderStatus.RECEIVED, order_items=[order_item])
        order.save()
        self.assertEqual(order.id, 1)
        # Change it an save it
        order.status = OrderStatus.PROCESSING
        order.save()
        self.assertEqual(order.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].status, OrderStatus.PROCESSING)

    def test_delete_a_order(self):
        """ Delete an order """
        order_item = OrderItem(product_id=1, name="Protein Bar (12 Count)", quantity=3, price=69.00)
        order = Order(customer_id=1, status=OrderStatus.RECEIVED, order_items=[order_item])
        order.save()
        self.assertEqual(len(order.all()), 1)
        # delete the order and make sure it isn't in the database
        order.delete()
        self.assertEqual(len(order.all()), 0)

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
        order = Order(customer_id=1, status=OrderStatus.RECEIVED)
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
        data = {'customer_id': 1, 'status': OrderStatus.RECEIVED, 'order_items': order_items}
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

    def test_deserialize_missing_key(self):
        """ Test deserialization of missing required keys """
        # missing customer id
        data = {'status': OrderStatus.RECEIVED}
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_find_order(self):
        """ Find a order by ID """
        Order(customer_id=1, status=OrderStatus.RECEIVED).save()
        other_order = Order(customer_id=2, status=OrderStatus.RECEIVED)
        other_order.save()
        order = Order.find(other_order.id)
        self.assertIsNot(order, None)
        self.assertEqual(order.id, other_order.id)
        self.assertEqual(order.status, OrderStatus.RECEIVED)

    def test_find_orders_since(self):
        """ Find an order since a date """
        for _ in list(range(5)):
            Order(customer_id=1, status=OrderStatus.RECEIVED).save()

        # create old order
        Order(customer_id=1, status=OrderStatus.RECEIVED, order_date=datetime.today() - timedelta(weeks=52)).save()

        self.assertEqual(len(Order.all()), 6)
        yesterday = date.today() - timedelta(days=1)
        self.assertEqual(len(Order.find_since(yesterday)), 5)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
