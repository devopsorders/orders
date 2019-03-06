"""
Models for Orders Service
All of the models are stored in this module
Models
------
Order - A Order used in the eCommerce web site backend

Attributes:
-----------
name (string) - the name of the pet
category (string) - the category the pet belongs to (i.e., dog, cat)
available (boolean) - True for pets that are available for adoption
"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Order(db.Model):
    """
    Class that represents an Order
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    # TODO table schema

    # def __repr__(self):
    #     return '<Order %r>' % (self.name)

    # def save(self):
    #     """
    #     Saves an Order to the data store
    #     """
    #     if not self.id:
    #         db.session.add(self)
    #     db.session.commit()
    #
    # def delete(self):
    #     """ Removes an Order from the data store """
    #     db.session.delete(self)
    #     db.session.commit()

    # def serialize(self):
    #     """ Serializes an Order into a dictionary """
    #     return {"id": self.id,
    #             "name": self.name,
    #             "category": self.category,
    #             "available": self.available}
    #
    # def deserialize(self, data):
    #     """
    #     Deserializes an Order from a dictionary
    #     Args:
    #         data (dict): A dictionary containing the Order data
    #     """
    #     try:
    #         self.name = data['name']
    #         self.category = data['category']
    #         self.available = data['available']
    #     except KeyError as error:
    #         raise DataValidationError('Invalid order: missing ' + error.args[0])
    #     except TypeError as error:
    #         raise DataValidationError('Invalid order: body of request contained bad or no data')
    #     return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    # return all orders

    # find order by id

    # find order or 404

    # find by some attribute such as status

    # find by ...
