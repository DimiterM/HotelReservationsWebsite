from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
	email = models.CharField(max_length=50)
	#password
	
	def __unicode__(self):
		return self.email
		
	def __str__(self):
		return self.unicode()
	

class Tag(models.Model):
	tag = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.tag
			
	def __str__(self):
		return self.unicode()


class Hotel(models.Model):
	name = models.CharField(max_length=25)
	stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	location = models.CharField(max_length=50)
	#photo
	text = models.CharField(max_length=150)
	tags = models.ManyToManyField(Tag)
	
	def __unicode__(self):
		return self.name + " (" + str(self.stars) + " stars) - " + self.location
			
	def __str__(self):
		return self.unicode()
	


class Room(models.Model):
	number = models.IntegerField(validators=[MinValueValidator(1)]) # TODO: make unique for hotel
	type = models.CharField(max_length=30)
	hotel = models.ForeignKey('Hotel')
	
	def __unicode__(self):
		return str(self.number) + ", " + self.type + " @ " + self.hotel.name
			
	def __str__(self):
		return self.unicode()


class Reservation(models.Model):
	start_date = models.DateField()
	end_date = models.DateField()
	user = models.ForeignKey('User')
	room = models.ForeignKey('Room')
	
	def __unicode__(self):
		return str(self.user) + " - from " + str(self.start_date) + " to " + str(self.end_date) + " in " + str(self.room)
		
	def __str__(self):
		return self.unicode()


