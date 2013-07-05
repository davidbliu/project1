from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# South for migrations
class Person(models.Model):
	user=models.ForeignKey(User, unique=True)
	friends=models.ManyToManyField('self',blank=True)
	def __str__(self):
		return '%s' % (self.user)

class Category(models.Model):
	type=models.CharField('type', max_length=200)

	def __str__(self):
		return '%s' % (self.type)


class Entry(models.Model):
	name=models.CharField('name', max_length=200, default='noname')
	category=models.ForeignKey(Category)
	date_added=models.DateField('date_added', blank=True, null=True)
	image=models.URLField(blank=False, unique=True)
	description=models.TextField('description', max_length=500, null=True, blank=True)

	def __str__(self):
		return '%s' % (self.name)
	
class Rating(models.Model):
	person=models.ForeignKey(Person);
	score=models.DecimalField(max_digits=20, decimal_places=3, default=0)
	entry=models.ForeignKey(Entry);
	def __str__(self):
		return '%s %s' % (self.person, self.entry)