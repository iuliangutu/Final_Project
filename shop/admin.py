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


# de adaugat mai multe categorii de produse (de ex: televizoare, laptopuri) - ok
# de modificat design-ul la pagina principala de produse
# optional* django how to send email pe google pentru a adauga functionalitatea de a trimite mail

# 18.01
# order status de colorat 'pending' cu galben si 'completed' cu verde (de adaugat 'if' in client_orders.html)
# de adaugat copyright si contact in base.html (footer)
# sending email, de intrat in setarile de la contul de google nou-creat si cautat optiunea dezactivare 'bifa de securitate'
# de configurat adresa de mail si mesajul care se afiseaza

# optional* formular de contact
# optional* sugestii de alte produse
# optional* de rezolvat cand stergem un obiect din cart sa ne recalculeze totalul


