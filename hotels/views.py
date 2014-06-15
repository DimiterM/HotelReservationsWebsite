from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from hotels.models import Hotel, Tag, Room, RoomType, Photo

from hotels.forms import SearchHotelForm, ReservationForm, AuthenticateUser, RegisterUser

from itertools import repeat

from hotels.helper_views import *


def index(request, page_num=1):
    data = request.GET if request.GET else None
    form = SearchHotelForm(data)
    
    if form.is_valid():
        if form.cleaned_data['tags']:
            hotels_list = Hotel.objects.filter(name__icontains=form.cleaned_data['name'], stars__gte=form.cleaned_data['stars'], location__icontains=form.cleaned_data['location'], tags__contains=form.cleaned_data['tags']).distinct()
        else:   # do not include tags in the query (because 'tags__contains=[]' return no hotels)
            hotels_list = Hotel.objects.filter(name__icontains=form.cleaned_data['name'], stars__gte=form.cleaned_data['stars'], location__icontains=form.cleaned_data['location']).distinct()
    
    else:
        page_num = int(page_num)
        previous = page_num - 1
        next = page_num + 1
        
        hotels_list = Hotel.objects.all()[((page_num - 1) * 10) : (page_num * 10 - 1)]
        
        form = SearchHotelForm()
    
    return render(request, "index.html", locals())


def hotel_info(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    photo_album = Photo.objects.filter(hotel=hotel_id)
    return render(request, "hotel-info.html", locals())


def login_view(request):
    login_data = request.POST if request.POST else None
    login_form = AuthenticateUser(login_data)

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/hotels/')
        else:
            return HttpResponse('<h1>401: Unauthorized</h1>Wrong username or password!', status=401)

    return render(request, "login.html", locals())


def register(request):
    register_data = request.POST if request.POST else None
    register_form = RegisterUser(register_data)

    if request.method == 'POST':
        if register_form.is_valid():
            register_form.save()
            return HttpResponse("Successfully registered! <a href=\"/hotels/login/\">Login!</a>")

    return render(request, "register.html", locals())


def reserve(request, hotel_id):
    hotel = Hotel.objects.filter(id=hotel_id)
    room_types = Room.objects.filter(hotel=hotel).values('type').distinct()
    
    data = request.POST if request.POST else None
    form = ReservationForm(data, extra=room_types)
    # dynamically generate 1 number field for each room type in this hotel
    
    if request.method == 'POST':
        if form.is_valid():
            # get rooms by type
            room_types = [RoomType.objects.get(id=rt['type']) for rt in room_types]

            rooms_to_save = []	# rooms_to_save = [ roomtype1, roomtype1, ..., roomtype2, roomtype2, ... ]
            free_rooms_of_type = []
            reservations = []

            for room in room_types:
                rooms_to_save += list(repeat(room.type, form.cleaned_data[room.type]))
                
            # foreach room in rooms_to_save make a separate reservation
            for room in rooms_to_save:
                free_rooms_of_type = get_free_rooms_of_type(hotel_id, form.cleaned_data['start_date'], form.cleaned_data['end_date'], room)
                
                if not free_rooms_of_type:
                    # the reservation is not possible,
                    # but we try to rearrange the previous ones
                    # and see if we can make them fit better
                    if interval_scheduling(hotel_id, room, form.cleaned_data['start_date'], form.cleaned_data['end_date']):
                        continue
                    # else
                    # delete all reservations from the current user request
                    # (because either they all succeed or none does)
                    for res_id in reservations:
                        r = Reservation.objects.get(id=res_id)
                        r.delete()
                    log = "Not enough free rooms!"
                    return render(request, "reserve.html", locals())
                else:
                    best_room_for_this = choose_best_room(free_rooms_of_type, form.cleaned_data['start_date'], form.cleaned_data['end_date'])
                    reservation = Reservation(start_date=form.cleaned_data['start_date'], end_date=form.cleaned_data['end_date'], user=request.user, room=best_room_for_this)
                    reservation.save()
                    reservations.append(reservation.id)
                    log = "Success!"
                    
        else:
            log = "Form is not valid!"
    
    return render(request, "reserve.html", locals())

