from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ['host','participants']
        # fields = '__all__'
        # fields = ['host','topic']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
