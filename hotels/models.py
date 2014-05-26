from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
	email = models.CharField(max_length=50)
	#password
	
	def __unicode__(self):
		return self.email
	

class Tag(models.Model):
	tag = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.tag


class Hotel(models.Model):
	name = models.CharField(max_length=25)
	stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	location = models.CharField(max_length=50)
	#photo
	text = models.CharField(max_length=150)
	tags = models.ManyToManyField(Tag)
	
	def __unicode__(self):
		return self.name + " (" + str(self.stars) + " stars) - " + self.location
	


class Room(models.Model):
	number = models.IntegerField(validators=[MinValueValidator(1)]) # TODO: make unique for hotel
	type = models.CharField(max_length=30)
	hotel = models.ForeignKey('Hotel')
	
	def __unicode__(self):
		return str(self.number) + ", " + self.type + " @ " + self.hotel.name


class Reservation(models.Model):
	start_date = models.DateField()
	end_date = models.DateField()
	user = models.ForeignKey('User')
	room = models.ForeignKey('Room')


