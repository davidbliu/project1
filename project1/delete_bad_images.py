from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person, Comment
from django import forms
from datetime import datetime
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
import StringIO
import struct
import urllib2

# import ImageFile
def getRemoteImageInfo(url):
    image = urllib2.urlopen(url)
    data = str(image.read(2))
    height = -1
    width = -1
    content_type = ''
    
    if data.startswith('\377\330'):
        content_type = 'image/jpeg'
        b = image.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = image.read(1)
                while (ord(b) == 0xFF): b = image.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    image.read(3)
                    h, w = struct.unpack(">HH", image.read(4))
                    break
                else:
                    image.read(int(struct.unpack(">H", image.read(2))[0])-2)
                b = image.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass
    return content_type, width, height


count=0
entries=Entry.objects.all()
for e in entries:
	link=e.image
	if ('.jpg' not in link) and ('.png' not in link) and ('.gif' not in link) and ('.jpeg' not in link):
		print link
		e.delete()
		count+=1
	if ('fanpop' in link):
		print link
		e.delete()
		count+=1
	# try:
	# 	a= getRemoteImageInfo(link)
	# 	print a
	# 	print a[0]
	# 	print a[1]
	# 	print a[2]
	# except:
	# 	print link
	# 	print e.id
	# 	print 'caused a problem'
print count
print 'were deleted'

