from django.forms import ModelForm
from django import forms
from .models import Hotel, Tag

class SearchHotel(ModelForm):
    #

    class Meta:
        model = Hotel
