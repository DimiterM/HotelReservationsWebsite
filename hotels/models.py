from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
	

class Tag(models.Model):
	tag = models.CharField(max_length=30)
	
	def __str__(self):
		return self.tag


class Hotel(models.Model):
	name = models.CharField(max_length=25)
	stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	location = models.CharField(max_length=50)
	#photo
	text = models.CharField(max_length=150)
	tags = models.ManyToManyField(Tag)
	
	def __str__(self):
	    return "{0} ({1} stars) - {2}".format(self.name, self.stars, self.location)


class Room(models.Model):
	number = models.IntegerField(validators=[MinValueValidator(1)]) # TODO: make unique for hotel
	type = models.CharField(max_length=30)
	hotel = models.ForeignKey('Hotel')
	
	def __str__(self):
	    return "{0}, {1} @ {2}".format(self.number, self.type, self.hotel.name)


class Reservation(models.Model):
	start_date = models.DateField()
	end_date = models.DateField()
	user = models.ForeignKey(User)
	room = models.ForeignKey('Room')
	
	def __str__(self):
	    return "{0} - from {1} to {2} in {3}".format(self.user, self.start_date, self.end_date, self.room)


