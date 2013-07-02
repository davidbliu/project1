# Create your views here.
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry
from django import forms
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf

def cat_list(request):
	response=HttpResponse()
	response.write("<html> <body> \n")
	response.write("<h1> Categories </h1> <hr>")
	cList=Category.objects.all()
	for c in cList:
		link = "<a href= \"info/%d\">" %(c.id)
		response.write("<li> %s%s</a></li>" % (link, c.type))
	response.write("</body></html>")
	return response
# def details(request, pID='0', opts=()):
# 	p=get_object_or_404(Person, pk=pID)
# 	return render_to_response('People/person_details.html', {'p':p})
	
def entry_detail(request, eID='0', opts=()):
	entry=get_object_or_404(Entry, pk=eID)
	return render_to_response('Rate/entry_detail.html', {'entry':entry})


class EntryForm(ModelForm):
	class Meta:
		model=Entry
		fields=[]
def entry_form(request, eID='0', opts=()):
	form=EntryForm()
	message='unknown request'
	entry=get_object_or_404(Entry, pk=eID)
	if request.method=='GET':
		form=EntryForm(instance=entry)
		message='Editing Entry %s ' % entry.name 
	if request.method=='POST':
		if request.POST['submit']=='1' or request.POST['submit']=='2' or request.POST['submit']=='3' or request.POST['submit']=='4' or request.POST['submit']=='5':
			message='Update request for %s' % entry.name
			form=EntryForm(request.POST.copy(), instance=entry)
			if form.is_valid():
				try:
					entry.rating= float(request.POST['submit'])
					form.save()
					message+=' Updated'
				except:
					message=' Database Error'
			else:
				message+='invalid'
	c={}
	c.update(csrf(request))
	c['eForm']=form
	c['message']=message
	return render_to_response('Rate/entry_form.html', c) 

