import profile

from accounts.models import Profile
from shop.models import Product, Order, OrderLine, Cart
from django.contrib.auth.models import User

# inainte de chatgpt
# class AddToCart:
#     def __init__(self, user):
#         self.user = user
#
#         # Ensure Profile exists
#         self.profile, created = Profile.objects.get_or_create(user=self.user)
#
#         self.order = Order.objects.filter(client=self.profile, status='pending').first()
#         if not self.order:
#             self.order = Order.objects.create(client=self.profile, status='pending')
#
#     def add_product(self, product_id, quantity, product_price):
#         product = Product.objects.get(pk=product_id)
#
#         cart = Cart.objects.filter(client=self.profile).first()
#         if not cart:
#             cart = Cart.objects.create(client=self.profile, order=self.order)
#
#         # Check if an OrderLine already exists for this product
#         order_line = cart.order_lines.filter(product=product).first()
#
#         if order_line:
#             order_line.quantity += quantity  # Update quantity
#             order_line.save()
#         else:
#             order_line = OrderLine.objects.create(  # Save directly to DB
#                 order=self.order,
#                 product=product,
#                 quantity=quantity,
#                 product_price=product_price  # Pass the correct number, NOT an Order!
#             )
#             cart.order_lines.add(order_line)  # Add to Cart AFTER saving to DB
#
#         self.recalculate_cost()
#         return order_line
#
#     # varianta inainte de chatgpt
#     # def recalculate_cost(self):
#     #     self.order.total_cost = sum(item.product.price * item.quantity for item in self.order.cart.order_lines.all())
#     #     self.order.save()
#     #     print("Your order is recalculated to have a total cost of:", self.order.total_cost)
#
#     # chatgpt
#     def recalculate_cost(self):
#         self.order.total_cost = sum(item.product.price * item.quantity for item in self.order.cart.order_lines.all())
#         self.order.save(update_fields=["total_cost"])  # Explicitly saving only the total_cost field
#         print("Your order is recalculated to have a total cost of:", self.order.total_cost)
#
#     def remove_product(self, product_id):
#         """Remove a product from the cart and recalculate total cost."""
#         product = Product.objects.get(pk=product_id)
#         order_line = self.order.order_lines.filter(product=product).first()
#
#         if order_line:
#             order_line.delete()  # Remove the product from the cart
#             self.recalculate_cost()  # Recalculate total cost after deletion
#
#             # Refresh order and queryset
#             self.order.refresh_from_db()
#             self.order.order_lines.all().refresh_from_db()
#
#             print(f"Product {product.name} removed. New total cost: {self.order.total_cost}")
#     def remove_product_and_display_total(self, product_id):
#         """Remove a product and print the updated total cost."""
#         self.remove_product(product_id)
#         print(f"Updated total cost: {self.order.total_cost}")

# chatGPT
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
        """Remove a product from the cart and recalculate total cost."""
        product = Product.objects.get(pk=product_id)
        order_line = self.order.order_lines.filter(product=product).first()

        if order_line:
            order_line.delete()  # Remove the product from the cart
            self.recalculate_cost()  # Recalculate the total cost

            # Refresh the order
            self.order.refresh_from_db()
            self.order.order_lines.all().refresh_from_db()

            print(f"Product {product.name} removed. New total cost: {self.order.total_cost}")


