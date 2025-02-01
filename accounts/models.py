from django.core.validators import MinLengthValidator, RegexValidator
from django.db.models import Model, OneToOneField, TextField, CASCADE, ForeignKey, DateTimeField, BooleanField, \
    CharField
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your models here.
class Profile(Model):

    user = OneToOneField(User, on_delete=CASCADE)
    address = TextField(blank=True, null=True)
    phone = CharField(
        max_length=15,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r'^\d+$', message="Phone number must contain only digits.")
        ]
    )
    def __str__(self):
        return self.user.username
