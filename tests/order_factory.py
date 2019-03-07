"""
Test Factory to make fake objects for testing
"""
# import factory
# from factory.fuzzy import FuzzyChoice, FuzzyInteger
# from app.models import Order, STATUS_DELIVERED, STATUS_PROCESSING, STATUS_RECEIVED, STATUS_SHIPPED
# from datetime import datetime
#
#
# class OrderItemFactory(factory.Factory):
#     """ Creates fake orders that don't cost any money """
#
#     class Meta:
#         model = Order
#
#     # TODO update this
#     id = factory.Sequence(lambda n: n)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
#     order = db.relationship('Order', back_populates='order_items')
#     product_id = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#
#
# class OrderFactory(factory.Factory):
#     """ Creates fake orders that don't cost any money """
#
#     class Meta:
#         model = Order
#
#     id = factory.Sequence(lambda n: n)
#     order_items = factory.SubFactory(OrderItemFactory)
#     customer_id = FuzzyInteger(1, 20)
#     order_date = factory.LazyFunction(datetime.now)
#     status = FuzzyChoice(choices=[STATUS_RECEIVED, STATUS_PROCESSING, STATUS_DELIVERED, STATUS_SHIPPED])
#
#
# if __name__ == '__main__':
#     for _ in range(10):
#         order = OrderFactory()
#         print(order.serialize())
