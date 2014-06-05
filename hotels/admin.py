from django.contrib import admin
from hotels.models import *


admin.site.register(Hotel)
admin.site.register(Tag)
admin.site.register(Room)
admin.site.register(Reservation)

