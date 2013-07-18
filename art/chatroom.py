from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.contrib.contenttypes import generic
from datetime import datetime

class RoomManager(models.Manager):
    '''Custom model manager for rooms, this is used for "table-level" operations.
    All methods defined here can be invoked through the Room.objects class.
    @see: http://docs.djangoproject.com/en/1.0/topics/db/managers/#topics-db-managers
    Also see GenericTypes from the contenttypes django app!
    @see: http://docs.djangoproject.com/en/1.0/ref/contrib/contenttypes/''' 

    def create(self, object):
        '''Creates a new chat room and registers it to the calling object'''
        r = self.model(content_object=object)
        r.save()
        return r

    def get_for_object(self, object):
        '''Try to get a room related to the object passed.'''
        return self.get(content_type=ContentType.objects.get_for_model(object), object_id=object.pk)

    def get_or_create(self, object):
        '''Save us from the hassle of validating the return value of get_for_object and create a room if none exists'''
        try:
            return self.get_for_object(object)
        except Room.DoesNotExist:
            return self.create(object)

class Room(models.Model):
    '''Representation of a generic chat room'''
    content_type = models.ForeignKey(ContentType) # to what kind of object is this related
    object_id = models.PositiveIntegerField() # to which instace of the aforementioned object is this related
    content_object = generic.GenericForeignKey('content_type','object_id') # use both up, USE THIS WHEN INSTANCING THE MODEL
    created = models.DateTimeField(default=datetime.now())
    comment = models.TextField(blank=True, null=True)
    objects = RoomManager() # custom manager

    def __add_message(self, type, sender, message=None):
        '''Generic function for adding a message to the chat room'''
        m = Message(room=self, type=type, author=sender, message=message)
        m.save()
        return m

    def say(self, sender, message):
        '''Say something in to the chat room'''
        return self.__add_message('m', sender, message)
    def join(self, user):
        '''A user has joined'''
        return self.__add_message('j', user)

    def leave(self, user):
        '''A user has leaved'''
        return self.__add_message('l', user)

    def messages(self, after_pk=None, after_date=None):
        '''List messages, after the given id or date'''
        m = Message.objects.filter(room=self)
        if after_pk:
            m = m.filter(pk__gt=after_pk)
        if after_date:
            m = m.filter(timestamp__gte=after_date)
        return m.order_by('pk')

    def last_message_id(self):
        '''Return last message sent to room'''
        m = Message.objects.filter(room=self).order_by('-pk')
        if m:
            return m[0].id
        else:
            return 0

    def __unicode__(self):
        return 'Chat for %s %d' % (self.content_type, self.object_id)