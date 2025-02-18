import profile

from accounts.models import Profile
from shop.models import Product, Order, OrderLine, Cart
from django.contrib.auth.models import User

class AddToCart:
    def __init__(self, user):
        self.user = user
        self.profile, created = Profile.objects.get_or_create(user=self.user)

        # Fetch the pending order, if one exists
        self.order = Order.objects.filter(client=self.profile, status='pending').first()

        if not self.order:
            # If no pending order exists, create a new one
            self.order = Order.objects.create(client=self.profile, status='pending')

    def add_product(self, product_id, quantity, product_price):
        product = Product.objects.get(pk=product_id)

        # Ensure the cart is created and linked to the pending order
        cart = Cart.objects.filter(client=self.profile).first()

        if not cart:
            # If cart doesn't exist, create one linked to the order
            cart = Cart.objects.create(client=self.profile, order=self.order)

        # Check if an OrderLine for this product already exists
        order_line = cart.order_lines.filter(product=product).first()

        if order_line:
            # Update quantity if product is already in the cart
            order_line.quantity += quantity
            order_line.save()
        else:
            # Create a new order line if product is not already in cart
            order_line = OrderLine.objects.create(
                order=self.order,
                product=product,
                quantity=quantity,
                product_price=product_price
            )
            cart.order_lines.add(order_line)  # Add to cart AFTER saving to DB

        self.recalculate_cost()  # Recalculate order total after adding product
        return order_line


    def recalculate_cost(self):
        # Update order total cost
        self.order.total_cost = sum(item.product.price * item.quantity for item in self.order.cart.order_lines.all())
        self.order.save(update_fields=["total_cost"])  # Save only the total cost field
        print("Your order is recalculated to have a total cost of:", self.order.total_cost)

    def remove_product(self, product_id):
        try:
            # Assuming you're deleting an order line by product_id
            order_line = OrderLine.objects.get(product_id=product_id, order=self.order)
            order_line.delete()
            self.order.save()  # Make sure the order's total cost is recalculated
        except OrderLine.DoesNotExist:
            pass  # Handle this case if needed


