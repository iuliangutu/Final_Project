import re
from datetime import date

from django.db.models import TextField
from django.forms import ModelForm, CharField, IntegerField, Form, DecimalField

from shop.models import Product


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    title = CharField(max_length=128)
    description = TextField()
    price = IntegerField()

    def clean(self):
        result = super().clean()
        # if result['order']:

        print(result)
        return result
