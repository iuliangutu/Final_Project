from django.contrib import admin

# Register your models here.
from .models import Category, Product, Seller, ProductType, Order, OrderLine, Cart

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(ProductType)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Cart)



