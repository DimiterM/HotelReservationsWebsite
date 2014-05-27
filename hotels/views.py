from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse

from hotels.models import Hotel, Tag

from hotels.forms import SearchHotelForm


#def index(request, page_num=1):
#	page_num = int(page_num)
#	previous = page_num - 1
#	next = page_num + 1
#	hotels_list = Hotel.objects.all()[((page_num-1) * 10) : (page_num * 10 - 1)]
#	tags_list = Tag.objects.all()
#	return render(request, "index.html", locals())

def index(request, page_num=1):
	data = request.POST if request.POST else None
	form = SearchHotelForm(data)
	
	if request.method == 'POST': #    => user searches hotels
		if form.is_valid():
			hotels_list = Hotel.objects.filter(name__icontains=form.cleaned_data['name'], stars__gte=form.cleaned_data['stars'], location__icontains=form.cleaned_data['location'])
			return render(request, "index.html", locals()) 
		else: None
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


def reserve(request, hotel_id):
    return render(request, "reserve.html", locals())


def login(request):
    return render(request, "login.html", locals())
    

def search(request):
    data = request.POST if request.POST else None
    form = SearchHotel(data)
    
#    if request.method == 'POST':
#        if form.is_valid():
#            form.save()
#            return redirect('index')
    
    return render(request, "index.html", locals())

