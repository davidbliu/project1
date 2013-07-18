from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
# South for migrations
class Message(models.Model):
	sender=models.ForeignKey(User, related_name='message_sender')
	reciever=models.ForeignKey(User, related_name='message_reciever')
	message=models.TextField(max_length=500, null=True, blank=True)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.message)


