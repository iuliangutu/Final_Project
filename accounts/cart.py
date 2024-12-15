from accounts.models import Profile
from shop.models import Product, Order, OrderLine
from django.contrib.auth.models import User

class AddToCart:
    def __init__(self, user):
        self.user = user
        self.profile = Profile.objects.get(user=self.user)
        self.order, created = Order.objects.get_or_create(client=self.profile, status='pending')

    def add_product(self, product_id, quantity, product_price):
        product = Product.objects.get(pk=product_id)
        order_line, created = OrderLine.objects.get_or_create(product=product, quantity=quantity, product_price=product_price)

        if created:
            order_line.quantity = quantity
        else:
            order_line.quantity += quantity

        order_line.product_price = self.order
        order_line.save()

        # Recalculează costul total al comenzii
        self.order.total_cost = sum(item.product.price * item.quantity for item in self.order.orderline_set.all())
        self.order.save()

        return order_line