from hotels.models import Hotel, Tag, Room, Reservation
from datetime import timedelta

def get_free_rooms_of_type(hotel_id, start_date, end_date, room_type):   
    all_rooms = Room.objects.filter(hotel=hotel_id, type=room_type)
    
    ids_rooms_taken_already = Reservation.objects.filter(room__type=room_type, room__hotel__id=hotel_id, start_date__lt=start_date, end_date__gte=start_date).values('room').distinct()
    ids_rooms_to_be_taken_soon = Reservation.objects.filter(room__type=room_type, room__hotel__id=hotel_id, start_date__lt=end_date, end_date__gte=start_date).values('room').distinct()
    
    unavailable_rooms = ids_rooms_taken_already | ids_rooms_to_be_taken_soon
    unavailable_rooms = [i['room'] for i in unavailable_rooms]
    
    return [x for x in all_rooms if x.id not in unavailable_rooms]


def choose_room_optimally(free_rooms_of_type, start_date, end_date):
    INTERVAL_TO_CHECK = 3
    
    busyness_of_rooms = []
    for room in free_rooms_of_type:
        reservations_starting_in_interval = Reservation.objects.filter(start_date__gte = start_date + timedelta(days=INTERVAL_TO_CHECK), start_date__lte =  end_date + timedelta(days=INTERVAL_TO_CHECK)).count()
        reservations_ending_in_interval = Reservation.objects.filter(end_date__gte = start_date + timedelta(days=INTERVAL_TO_CHECK), end_date__lte =  end_date + timedelta(days=INTERVAL_TO_CHECK)).count()
        busyness_of_rooms.append(reservations_starting_in_interval + reservations_ending_in_interval)
    
    index_of_optimal = busyness_of_rooms.index(min(busyness_of_rooms))
    return free_rooms_of_type[index_of_optimal]
