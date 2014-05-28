from django.forms import ModelForm
from django import forms
from hotels.models import Hotel, Tag
from django.contrib.auth.models import User

class SearchHotelForm(ModelForm):
    name = forms.CharField(label='Hotel name', required=False)
    stars = forms.IntegerField(label='Stars (minimum)', initial=1)
    location = forms.CharField(label='Location', required=False)
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Hotel
        exclude = ['text', 'photo']


class AuthenticateUser(ModelForm):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField(label='E-mail')
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class RegisterUser(ModelForm):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField(label='E-mail')
    first_name = forms.CharField(label='First name', required=False)
    last_name = forms.CharField(label='Last name', required=False)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
