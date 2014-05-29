from hotels.models import Hotel, Tag, Room, Reservation

def get_free_rooms_of_type(hotel_id, start_date, end_date, room_type):   
    all_rooms = Room.objects.filter(hotel=hotel_id, type=room_type)
    
    ids_rooms_taken_already = Reservation.objects.filter(room__type=room_type, room__hotel__id=hotel_id, start_date__lt=start_date, end_date__gte=start_date).values('room').distinct()
    ids_rooms_to_be_taken_soon = Reservation.objects.filter(room__type=room_type, room__hotel__id=hotel_id, start_date__lt=end_date, end_date__gte=start_date).values('room').distinct()
    
    unavailable_rooms = ids_rooms_taken_already | ids_rooms_to_be_taken_soon
    unavailable_rooms = [i['room'] for i in unavailable_rooms]
    
    return [x for x in all_rooms if x.id not in unavailable_rooms]
