from django.forms import ModelForm
from django import forms
from hotels.models import Hotel, Tag, Reservation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SearchHotelForm(ModelForm):
    name = forms.CharField(label='Hotel name', required=False)
    stars = forms.IntegerField(label='Stars (minimum)', initial=1)
    location = forms.CharField(label='Location', required=False)
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Hotel
        exclude = ['text', 'photo']


class ReservationForm(ModelForm):
    start_date = forms.DateField(label='First day')
    end_date = forms.DateField(label='Last day')
    
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra') if 'extra' in kwargs else {}
        super(ReservationForm, self).__init__(*args, **kwargs)
        
        for room_type in extra:
            self.fields[room_type['type']] = forms.IntegerField(label=room_type['type'], initial=0)
    
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']


class AuthenticateUser(ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterUser(UserCreationForm):
    email = forms.EmailField(label='E-mail')
    first_name = forms.CharField(label='First name', required=False)
    last_name = forms.CharField(label='Last name', required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterUser, self).__init__(*args, **kwargs)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
