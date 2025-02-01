from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CharField, Model, ForeignKey, DO_NOTHING, IntegerField, DateField, TextField, \
    DateTimeField, SlugField, URLField, ManyToManyField, CASCADE, OneToOneField, PositiveIntegerField, DecimalField

import shop.models
from accounts.models import Profile

# Create your models here.

ORDER_STATUS_CHOICES = [('pending', 'Pending'), ('payment', 'Payment Confirmation'),
                        ('shipped', 'Shipped'), ('status', 'Order Status'), # de adaugat redirect catre firma de curierat cu AWB
                        ('delivered', 'Delivered'), ('cancelled', 'Cancelled'),]


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
    product_image = URLField(blank=True, null=True)
    category = ForeignKey(Category, on_delete=CASCADE)
    price = IntegerField()
    product_type = ForeignKey(ProductType, on_delete=CASCADE)
    seller = ForeignKey(Seller, on_delete=CASCADE)
    rating = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.title

class Order(Model):
    total_cost = IntegerField(default=0)
    delivery_address = TextField(default='')
    order_date = DateTimeField(auto_now_add=True)
    client = ForeignKey(Profile, on_delete=CASCADE)
    status = CharField(max_length=128, choices=ORDER_STATUS_CHOICES)

    def __str__(self):
        return f"Order id #{self.id}"


class OrderLine(Model):
    order = ForeignKey('shop.Order', on_delete=CASCADE)
    product = ForeignKey('shop.Product', on_delete=CASCADE)
    quantity = IntegerField()
    product_price = DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.product_price

    def __str__(self):
        return f"{self.quantity} x {self.product.title} at {self.product_price} each"



class Cart(Model):
    order = OneToOneField(Order, on_delete=CASCADE)
    order_lines = ManyToManyField(OrderLine)
    client = OneToOneField(Profile, on_delete=CASCADE)

    def __str__(self):
        return f"Cart for Order #{self.order.id} User {self.client}"





