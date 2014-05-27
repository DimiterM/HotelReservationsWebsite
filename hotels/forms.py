from django.forms import ModelForm
from django import forms
from hotels.models import Hotel, Tag

class SearchHotelForm(ModelForm):
    name = forms.CharField(label='Hotel name', required=False)
    stars = forms.IntegerField(label='Stars (minimum)', initial=1)
    location = forms.CharField(label='Location', required=False)
    tags_list = Tag.objects.all() # ??? TODO !!!

    class Meta:
        model = Hotel
        exclude = ['text', 'photo']
