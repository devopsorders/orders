"""
Models for Orders Service
All of the models are stored in this module
Models
------
Order - A Order used in the eCommerce web site backend

Attributes:
-----------
customer_id (string) - id of the customer
order_date (datetime) - date and time when the order was placed
status (string) - status of the order
order_items (relationship) - the collection of items that are part of this order


OrderItem - A OrderItem used in the eCommerce web site backend

Attributes:
-----------
order_id (fk integer) - id of the associated order
product_id (integer) - the id of product for this order item
name (string) - name of the product for this order item
quantity (integer) - quantity of the product for this order item
price (float) - price of the product at the time of this order item
"""
import logging

from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class OrderStatus:
    RECEIVED = 'received'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class Order(db.Model):
    """
    Class that represents an Order
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    status = db.Column(db.String(63), nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return '<Order: %d - Ordered on: %s>' % (self.id, self.order_date)

    def save(self):
        """
        Saves an Order to the data store
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes an Order from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes an Order into a dictionary """
        return {"id": self.id,
                "customer_id": self.customer_id,
                "order_date": self.order_date,
                "status": self.status,
                "order_items": [order_item.serialize() for order_item in self.order_items]}

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary
        Args:
            data (dict): A dictionary containing the Order data
        """
        try:
            self.customer_id = data['customer_id']
            self.status = data['status']
            for order_item in data['order_items']:
                self.order_items.append(OrderItem(product_id=order_item['product_id'],
                                                  name=order_item['name'],
                                                  quantity=order_item['quantity'],
                                                  price=float(order_item['price'])))
        except KeyError as error:
            raise DataValidationError('Invalid order: missing ' + error.args[0])
        except TypeError:
            raise DataValidationError('Invalid order: body of request contained bad or no data')
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Orders in the database """
        cls.logger.info('Processing all Orders')
        return cls.query.all()

    @property
    def total(self):
        order_total = 0
        for order_item in self.order_items:
            order_total += order_item.total
        return order_total

    # return all orders

    @classmethod
    def find(cls, order_id):
        """ Finds an order by it's ID """
        cls.logger.info('Processing lookup for id %s ...', order_id)
        return cls.query.get(order_id)

    @classmethod
    def find_or_404(cls, order_id):
        """ Find a order by it's id """
        cls.logger.info('Processing lookup or 404 for id %s ...', order_id)
        return cls.query.get_or_404(order_id)

    # find by some attribute such as status

    # find by ...


class OrderItem(db.Model):
    """
    Class that represents an Order Item
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    # order = db.relationship('Order', back_populates='order_items')  # TODO this doesn't work right now
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(63), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Order Id: %d - Product Id: %s>' % (self.order_id, self.product_id)

    @property
    def total(self):
        return round(self.price * self.quantity, 2)

    def serialize(self):
        """ Serializes an OrderItem into a dictionary """
        return {'id': self.id,
                'order_id': self.order_id,
                'product_id': self.product_id,
                'name': self.name,
                'quantity': self.quantity,
                'price': self.price}
