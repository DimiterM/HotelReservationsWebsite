from hotels.models import Hotel, Tag, RoomType, Room, Reservation
from datetime import timedelta

def get_free_rooms_of_type(hotel_id, start_date, end_date, room_type):
    """
    Given a hotel, room type and the time interval for the reservation
    it retrieves from the database a list of all rooms (in that hotel 
    of that type) that are unoccupied for that time
    
    Algorithm:
    1. Get all rooms in that hotel of that type (roomtype.id)
    2. Get all rooms in the hotel which are taken before start_date and
    will not be released before end_date
    3. Get all rooms in the hotel which will be taken taken after start_date and
    before end_date
    4. Union of the querysets in 2. & 3.
    5. Difference of the querysets 1. & 4.
    """
    room_type = RoomType.objects.get(type=room_type)
    room_type = room_type.id

    all_rooms = Room.objects.filter(hotel=hotel_id, type=room_type)
    
    ids_rooms_taken_already = Reservation.objects.filter(room__type=room_type, room__hotel__id=hotel_id, start_date__lt=start_date, end_date__gte=start_date).values('room').distinct()
    ids_rooms_to_be_taken_soon = Reservation.objects.filter(room__type=room_type, room__hotel__id=hotel_id, start_date__lt=end_date, end_date__gte=start_date).values('room').distinct()
    
    unavailable_rooms = ids_rooms_taken_already | ids_rooms_to_be_taken_soon
    unavailable_rooms = [i['room'] for i in unavailable_rooms]
    
    return [x for x in all_rooms if x.id not in unavailable_rooms]


def choose_room_optimally(free_rooms_of_type, start_date, end_date):
    """
    Out of all free rooms candidates to be reserved now
    choose one so that future reservations have a better chance to be satisfied.

    If we used a greedy algorithm, it would be possible to have such reservations
    which make it impossible for other reservations to happen.
    Example:
    reservation1 = day1 - day2
    reservation2 = day4 - day5
    reservation3 = day2 - day4

        Greedy alogrithm:
        days:  1     2     3     4     5
        room1: Taken Taken Free  Free  Free
        room2: Free  Free  Free  Taken Taken
        (reservation3 fails)

        This:
        days:  1     2     3     4     5
        room1: Taken Taken Free  Taken Taken
        room2: Free  Taken Taken Taken Free
        (success)
        We make the schedules more compact by choosing the room so that
        more rooms will have big intervals of free time.

    Basic idea: We don't choose simply a room free between
    start_date & end_date. We count the number of reservations for that room
    in the interval (start_date - several days) & (end_date + several days).
    We choose the room that has the maximum value.
    """
    INTERVAL_TO_CHECK = 3
    
    busyness_of_rooms = []
    for room in free_rooms_of_type:
        reservations_starting_in_interval = Reservation.objects.filter(start_date__gte = start_date + timedelta(days=INTERVAL_TO_CHECK), start_date__lte =  end_date + timedelta(days=INTERVAL_TO_CHECK)).count()
        reservations_ending_in_interval = Reservation.objects.filter(end_date__gte = start_date + timedelta(days=INTERVAL_TO_CHECK), end_date__lte =  end_date + timedelta(days=INTERVAL_TO_CHECK)).count()
        busyness_of_rooms.append(reservations_starting_in_interval + reservations_ending_in_interval)
    
    index_of_optimal = busyness_of_rooms.index(min(busyness_of_rooms))
    return free_rooms_of_type[index_of_optimal]
