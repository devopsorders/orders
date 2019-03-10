"""
Test Factory to make fake objects for testing
"""
import random
from datetime import datetime

import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyFloat

from app.models import Order, OrderItem, OrderStatus

PRODUCTS = [
    {'product_id': 1, 'name': 'Kindle'},
    {'product_id': 2, 'name': 'AirPods'},
    {'product_id': 3, 'name': 'Soap'},
    {'product_id': 4, 'name': 'MacBook Air'},
    {'product_id': 5, 'name': 'Dog Food'},
    {'product_id': 6, 'name': '75" TV'},
    {'product_id': 7, 'name': 'Mattress'},
    {'product_id': 8, 'name': 'Protein Bars'},
    {'product_id': 9, 'name': 'Notebook'},
    {'product_id': 10, 'name': 'AA Batteries'}
]


def get_product_name(product_id):
    for product in PRODUCTS:
        if product['product_id'] == product_id:
            return product['name']

    raise KeyError


class OrderFactory(factory.Factory):
    """ Creates fake orders that don't cost any money """

    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n + 1)  # +1 so id don't start at 0
    customer_id = FuzzyInteger(1, 20)
    order_date = factory.LazyFunction(datetime.now)
    status = FuzzyChoice(
        choices=[OrderStatus.RECEIVED, OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED])

    # order_items = factory.RelatedFactory(OrderItemFactory, 'order_items', action=models.UserLog.ACTION_CREATE)

    @factory.post_generation
    def order_items(self, create, extracted, **kwargs):
        if not create:
            return

        # add 1 to 3 order items to each order
        for _ in list(range(random.randint(1, 3))):
            self.order_items.append(OrderItemFactory.create(order_id=self.id))


class OrderItemFactory(factory.Factory):
    """ Creates fake order items to go with an order"""

    class Meta:
        model = OrderItem

    id = factory.Sequence(lambda n: n + 1)
    order_id = factory.SubFactory(OrderFactory)
    product_id = FuzzyInteger(1, len(PRODUCTS) - 1)
    name = factory.LazyAttribute(lambda o: get_product_name(o.product_id))
    quantity = FuzzyInteger(1, 3)
    price = FuzzyFloat(0.01, 99, precision=4)

    @factory.post_generation
    def order_id(self, create, extracted, **kwargs):
        if not create:
            return

        self.order_id = extracted


if __name__ == '__main__':
    for _ in range(10):
        order = OrderFactory()
        print(order.serialize())
