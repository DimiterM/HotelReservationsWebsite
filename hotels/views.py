from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from hotels.models import Hotel

def index(request, page_num=1):
	page_num = int(page_num)
	previous = page_num - 1
	next = page_num + 1
	hotels_list = Hotel.objects.all()[((page_num-1) * 10) : (page_num * 10 - 1)]
	return render(request, "index.html", locals())


def hotel_info(request, hotel_id):
	hotel = get_object_or_404(Hotel, id=hotel_id)
	return render(request, "hotel-info.html", locals())


def reserve(request, hotel_id):
    return render(request, "reserve.html", locals())


def login(request):
    return render(request, "login.html", locals())