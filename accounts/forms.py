from django.contrib.auth.forms import UserCreationForm
from django.db.models import Min
from django.db.models.expressions import result
from django.db.transaction import atomic
from django.forms import CharField, Textarea, ModelForm, IntegerField
from django.http import request

from accounts.models import Profile


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ['first_name', 'last_name', 'email', 'username']

    phone = IntegerField()
    address = CharField(label='Introduce your address: ', widget=Textarea)

    @atomic
    def save(self, commit=True):

        result = super().save(commit)

        address = self.cleaned_data['address']
        phone = self.cleaned_data['phone']

        profile = Profile(address=address, phone=phone, user=result)
        if commit:
            profile.save()

        return result

    ## de adaugat functionalitatea cum ca utilizatorul poate primi mesaje de la vanzator

