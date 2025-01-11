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


# de adaugat mesajul 'va multumim pentru cumparaturi' dupa apasarea butonului 'payment'
# de adaugat 'Previous_Orders' in my profile
# care sa preia datele din 'cart' sa le stocheze cu id-ul de comanda si sa stearga automat
# de adaugat sugestii de produse in 'cart'

