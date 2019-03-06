"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from app.models import Order


class OrderFactory(factory.Factory):
    """ Creates fake orders that don't cost any money """

    class Meta:
        model = Order

    # TODO update this
    id = factory.Sequence(lambda n: n)
    # name = factory.Faker('first_name')
    # category = FuzzyChoice(choices=['dog', 'cat', 'bird', 'fish'])
    # available = FuzzyChoice(choices=[True, False])


if __name__ == '__main__':
    for _ in range(10):
        order = OrderFactory()
        print(order.serialize())
