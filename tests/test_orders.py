"""
Test cases for Order Model
Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
#from app.models import Order, DataValidationError, db
from app import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')


######################################################################
#  T E S T   C A S E S
######################################################################
# class TestOrders(unittest.TestCase):
#     """ Test Cases for Orders """
#
#     @classmethod
#     def setUpClass(cls):
#         """ These run once per Test suite """
#         app.debug = False
#         # Set up the test database
#         app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
#
#     @classmethod
#     def tearDownClass(cls):
#         pass
#
#     def setUp(self):
#         Order.init_db(app)
#         db.drop_all()  # clean up the last tests
#         db.create_all()  # make our sqlalchemy tables
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
