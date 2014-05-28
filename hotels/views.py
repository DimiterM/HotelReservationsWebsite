from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse

from hotels.models import Hotel, Tag

from hotels.forms import SearchHotelForm, AuthenticateUser, RegisterUser


def index(request, page_num=1):
	data = request.POST if request.POST else None
	form = SearchHotelForm(data)
	
	if request.method == 'POST': #    => user searches hotels
		if form.is_valid():
			hotels_list = Hotel.objects.filter(name__icontains=form.cleaned_data['name'], stars__gte=form.cleaned_data['stars'], location__icontains=form.cleaned_data['location'], tags__contains=form.cleaned_data['tags']).distinct()
			return render(request, "index.html", locals()) 
		else:
		    None
	else: # request.method == 'GET'    => user accesses main page
		page_num = int(page_num)
		previous = page_num - 1
		next = page_num + 1
		
		hotels_list = Hotel.objects.all()[((page_num-1) * 10) : (page_num * 10 - 1)]
		
		form = SearchHotelForm()
		return render(request, "index.html", locals())

	return render(request, "index.html", locals()) 

def hotel_info(request, hotel_id):
	hotel = get_object_or_404(Hotel, id=hotel_id)
	return render(request, "hotel-info.html", locals())


def login(request):
	login_data = request.GET if request.GET else None
	login_form = AuthenticateUser(login_data)
	
	register_data = request.POST if request.POST else None
	register_form = RegisterUser(register_data)
	
	if request.method == 'GET':	# user logs in
		None
	elif request.method == 'POST':		# new user registers
		None
# https://docs.djangoproject.com/en/1.6/topics/auth/default/#user-objects
	return render(request, "login.html", locals())


def reserve(request, hotel_id):
    return render(request, "reserve.html", locals())
    

