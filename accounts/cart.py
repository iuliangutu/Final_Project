from accounts.models import Profile
from shop.models import Product, Order, OrderLine, Cart
from django.contrib.auth.models import User

class AddToCart:
    def __init__(self, user):
        self.user = user
        self.profile = Profile.objects.get(user=self.user)
        self.order = Order.objects.filter(client=self.profile, status='pending').latest('order_date')

    def add_product(self, product_id, quantity, product_price):
        product = Product.objects.get(pk=product_id)

        if not self.order:
            self.order = Order.objects.create(client=self.profile, status='pending')

        # Verifică dacă există deja un OrderLine pentru acest produs în comanda curentă
        cart, created = Cart.objects.get_or_create(order=self.order, client=self.profile)
        order_line = cart.order_lines.all().filter(product=product).first()
        if order_line:
            # Dacă există, actualizează cantitatea
            order_line.quantity += quantity
        else:
            # Dacă nu există, creează un nou OrderLine
            order_line = OrderLine(product=product, quantity=quantity, product_price=product_price)
        order_line.save()
        cart.order_lines.add(order_line)
        print(cart)

        self.recalculate_cost()
        return order_line

    def recalculate_cost(self):
        self.order.total_cost = sum(item.product.price * item.quantity for item in self.order.orderline_set.all())
        self.order.save()
        print("Your order is recalculated to have a total cost of:", self.order.total_cost)
