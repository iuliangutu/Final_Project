from django.contrib import admin

# Register your models here.
from .models import Client, Category, Product, Provider, ProductType, Order, OrderLine, Cart

admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Provider)
admin.site.register(ProductType)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Cart)

