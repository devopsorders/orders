"""
Order Service
Paths:
------
GET /orders - Returns a list all of Orders
GET /orders/{id} - Returns the Order with a given id number
POST /orders - creates a new Order record in the database
PUT /orders/{id} - update a complete order
PATCH /orders/{id} - update part of an order
DELETE /orders/{id} - delete an order
PUT /orders/{id}/cancel - cancel an order
"""

import logging
import sys
from datetime import datetime

from flask import jsonify, request, abort, url_for, make_response
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from .models import Order, DataValidationError, OrderStatus

# Import Flask application
from . import app

# kind of hacky, but now all urls will work
app.url_map.strict_slashes = False

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad requests with 400_BAD_REQUEST """
    message = str(error)  # error.message or str(error) # TODO this might need to be put back for certain tests
    app.logger.warning(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST,
                   error='Bad Request',
                   message=message), status.HTTP_400_BAD_REQUEST


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND,
                   error='Not Found',
                   message=message), status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                   error='Method not Allowed',
                   message=message), status.HTTP_405_METHOD_NOT_ALLOWED


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                   error='Unsupported media type',
                   message=message), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR


######################################################################
# GET INDEX
######################################################################
@app.route('/', methods=['GET'])
def index():
    """ Root URL response """
    return app.send_static_file('index.html')


# @app.route('/')
# def index():
#     """ Root URL response """
#     return jsonify(name='Orders REST API Service',
#                    version='1.0',
#                    paths=url_for('list_orders', _external=True)
#                    ), status.HTTP_200_OK


######################################################################
# LIST ALL ORDERS
######################################################################
@app.route('/orders', methods=['GET'])
def list_orders():
    """ Returns all of the Orders """
    app.logger.info('Request for order list')
    order_status = request.args.get('status')
    orders_since = request.args.get('orders_since')

    if order_status:
        orders = Order.find_by_status(order_status)
    elif orders_since:
        orders_since_date = datetime.strptime(orders_since, '%Y-%m-%d').date()
        orders = Order.find_since(orders_since_date)
    else:
        orders = Order.all()

    results = [order.serialize() for order in orders]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE AN ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_orders(order_id):
    """
    Retrieve a single order
    This endpoint will return a order based on it's id
    """
    app.logger.info('Request for order with id: %s', order_id)
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW ORDER
######################################################################
@app.route('/orders', methods=['POST'])
def create_orders():
    """
    Creates an Order
    This endpoint will create an Order based the data in the body that is posted
    """
    app.logger.info('Request to create an order')
    check_content_type('application/json')
    order = Order()
    order.deserialize(request.get_json())
    order.save()
    message = order.serialize()
    location_url = url_for('get_orders', order_id=order.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })


######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_orders(order_id):
    """
    Update an Order
    This endpoint will update a Order based the body that is posted
    """
    app.logger.info('Request to update order with order id: %s', order_id)
    check_content_type('application/json')
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    # this is a bit of a hack, but since full order is posted, delete order items so not duplicated
    order.order_items.delete()
    # now deserialize json
    order.deserialize(request.get_json())
    order.id = order_id
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_orders(order_id):
    """
    Delete an order
    This endpoint will delete an order based the id specified in the path
    """
    app.logger.info('Request to delete order with id: %s', order_id)
    order = Order.find(order_id)
    if order:
        order.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
# CANCEL AN ORDER
######################################################################
@app.route('/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_orders(order_id):
    """
    Cancel an order
    This endpoint will cancel an order and notify any other systems
    """
    app.logger.info('Request to cancel order with id: %s', order_id)
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))

    # TODO should probably check to make sure this order hasn't been shipped or delivered first
    order.id = order_id
    order.status = OrderStatus.CANCELED
    order.save()
    # Notify other systems like shipping/billing of cancellation...
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initializes the SQLAlchemy app """
    # global app
    Order.init_db(app)


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))


def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')
