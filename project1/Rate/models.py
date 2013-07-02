from django.db import models

# Create your models here.
# South for migrations

class Category(models.Model):
	type=models.CharField('type', max_length=200)

	def __str__(self):
		return '%s' % (self.type)


class Entry(models.Model):
	name=models.CharField('name', max_length=200)
	category=models.ForeignKey(Category)
	date_added=models.DateField('date_added', blank=True, null=True)
	num_ratings=models.PositiveIntegerField('num_ratings', default=0)
	rating=models.DecimalField(max_digits=20, decimal_places=3)
	image=models.CharField('image', max_length=100)
	description=models.TextField('description', max_length=500, null=True)

	def __str__(self):
		return '%s' % (self.name)
	
