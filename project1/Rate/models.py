from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
# South for migrations
class Person(models.Model):
	user=models.ForeignKey(User, unique=True)
	friends=models.ManyToManyField('self',blank=True)
	avatar=models.URLField(blank=True, null=True)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.user)

class Category(models.Model):
	type=models.CharField('type', max_length=200)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.type)

class Entry(models.Model):
	name=models.CharField('name', max_length=200, default='no name')
	category=models.ForeignKey(Category)
	image=models.URLField(blank=False, unique=True)
	img=models.ImageField(upload_to= 'imgdb/', blank=True, null=True)
	description=models.TextField('description', max_length=500, null=True, blank=True)
	added_by=models.ForeignKey(Person)
	date_added = models.DateTimeField('date_added',auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	score=models.DecimalField(max_digits=20, decimal_places=3, default=0)
	def __str__(self):
		return '%s' % (self.name)
	
class Rating(models.Model):
	person=models.ForeignKey(Person);
	score=models.DecimalField(max_digits=20, decimal_places=3, default=0)
	entry=models.ForeignKey(Entry);
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s %s' % (self.person, self.entry)
		
class Comment(models.Model):
	person=models.ForeignKey(Person);
	comment=models.TextField('description', max_length=500, null=True, blank=True)
	entry=models.ForeignKey(Entry);
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	likers=models.CommaSeparatedIntegerField(max_length=10000000, blank=True)
	dislikers=models.CommaSeparatedIntegerField(max_length=10000000,blank=True)
	likes=models.DecimalField(max_digits=20, decimal_places=3, default=0)
	dislikes=models.DecimalField(max_digits=20, decimal_places=3, default=0)
	score=models.DecimalField(max_digits=20, decimal_places=3, default=0)
	def __str__(self):
		return '%s %s' % (self.person, self.entry)

class Saved(models.Model):
	person=models.ForeignKey(Person)
	layout=models.TextField( max_length=50000000, null=True, blank=True)
	entry=models.ForeignKey(Entry)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
