from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import CharField, Model, ForeignKey, DO_NOTHING, IntegerField, DateField, TextField, \
    DateTimeField, SlugField, URLField, ManyToManyField, CASCADE, OneToOneField

# Create your models here.

ORDER_STATUS_CHOICES = [('pending', 'Pending'), ('payment', 'Payment Confirmation'),
                        ('shipped', 'Shipped'), ('status', 'Order Status'), # de adaugat redirect catre firma de curierat cu AWB
                        ('delivered', 'Delivered'), ('cancelled', 'Cancelled'),]

# class Client(Model):
#     class Meta:
#         verbose_name_plural = "Client"
#
#     username = CharField(max_length=128)
#     address = TextField()
#     phone = CharField(max_length=15, validators=[MinLengthValidator(10)])
#

class Category(Model):
    class Meta:
        verbose_name_plural = "Category"

    name = CharField(max_length=128)

    def __str__(self):
        return self.name


class Seller(Model):
    seller = CharField(max_length=128)
    logo = URLField(blank=True, null=True)

    def __str__(self):
        return self.seller

class ProductType(Model):
    name = CharField(max_length=128)

    def __str__(self):
        return self.name


class Product(Model):
    title = CharField(max_length=128)
    description = TextField()
    thumbnail = URLField(blank=True, null=True)
    category = ForeignKey(Category, on_delete=CASCADE)
    price = IntegerField()
    product_type = ForeignKey(ProductType, on_delete=CASCADE)
    seller = ForeignKey(Seller, on_delete=CASCADE)

    def __str__(self):
        return self.title


class OrderLine(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    number_of_products = IntegerField()
    # product_price = IntegerField()


class Order(Model):
    username = CharField(max_length=128)
    total_cost = IntegerField()
    delivery_address = TextField()
    user_address = TextField()
    order_date = DateTimeField(auto_now_add=True)
    order_lines = ForeignKey(OrderLine, on_delete=CASCADE)
    # client = ForeignKey(Client, on_delete=CASCADE)
    status = CharField(max_length=128, choices=ORDER_STATUS_CHOICES)

    def __str__(self):
        return f"Order id #{self.id}"


class Cart(Model):
    order = OneToOneField(Order, on_delete=models.CASCADE)
    order_lines = ManyToManyField(OrderLine)

    def __str__(self):
        return f"Cart for Order #{self.order.id}"








