from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person
from django import forms
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory

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
				# try:
				rating= float(request.POST['submit'])
				new_rating=Rating(person=Person.objects.all()[0], entry=entry, score=rating);
				new_rating.save()
				form.save()
				return HttpResponseRedirect('/entry/%s/' % entry.id)
				message+=' Updated'
				# except:
				# 	message=' Database Error'
			else:
				message+='invalid'
	c={}
	c.update(csrf(request))
	c['eForm']=form
	c['message']=message
	return render_to_response('Rate/entry_form.html', c) 

def rate_form(request):
	form=EntryForm()
	message='unknown request'
	# entry=get_object_or_404(Entry, pk=eID)

	if request.method=='GET':
		# form=EntryForm(instance=entry)
		print('hello there GET METHOD')
		message='Editing Entry' 
	if request.method=='POST':
		print('POSTPOSTPOSTPOSTPOST')
		print(request.POST['submit'])
		print(request.session)
		message='post'
		return HttpResponseRedirect('/categories/')
	c={}
	c.update(csrf(request))
	c['eForm']=form
	c['message']=message
	return render_to_response('Rate/rate_form.html', c) 

def add_form(request):
	return render_to_response('Rate/rate_form.html')

class RatingForm(ModelForm):
	class Meta:
		model=Rating
		fields=['score']
class CustomRatingForm(ModelForm):
	entry=forms.URLField()
	def save(self, commit=True):
		entry=Entry.objects.get(name=self.cleaned_data['entry'])
		instance=super(CustomForm, self).save(commit=commit)
		instance.entry=entry
		if commit:
			instance.save()
		return instance
	class Meta:
		model=Rating
		fields=['score','person']
def rate_formset(request, eID=0):

	formsList=[]
	entries=Entry.objects.all()
	for entry in entries:
		form = RatingForm(initial={'entry':entry, 'person': Person.objects.all().get(id=1)})
		formsList.append(form)
	print(formsList)
	print('that ^ was the forms list')
	if request.method=='POST':
		if request.POST['submit']=='update':
			# formset=RateFormSet(request.POST.copy())
			print('update request 123456789')
	c={}
	c.update(csrf(request))
	c['formsList']=formsList
	# c['entry']=entry
	return render_to_response('Rate/rate_formset.html', c) 
	# RateFormSet=formset_factory(RateForm)
	# formset=RateFormSet()
	# # for form in formset:
	# # 	print(form.as_table())
	# entry=get_object_or_404(Entry, pk=eID)
	# person=Person.objects.get(id=1)
	# rating=Rating.objects.get(person=person, entry=entry)
	# form=RatingForm(instance=rating)
	# if request.method=='GET':
	# 	form=RatingForm(instance=rating)
	# if request.method=='POST':
	# 	if request.POST['submit']=='update':
	# 		form=RatingForm(request.POST.copy(), instance=rating)
	# 		if form.is_valid():
	# 			form.save()
	# c={}
	# c.update(csrf(request))
	# c['form']=form
	# c['entry']=entry
	# return render_to_response('Rate/rate_formset.html', c) 


class CustRateForm(ModelForm):
	class Meta:
		model=Rating
		CHOICES = ((1, "1",), (2, '2',), (3, '3',), (4, '4',), (5, '5',))
		fields=['score','person','entry']
		widgets={
			'score': forms.RadioSelect(choices=CHOICES),
			'person':forms.HiddenInput(),
			'entry':forms.HiddenInput()
		}
def rate_form3(request, pID=1):
	entries=Entry.objects.all()
	forms={}
	for entry in entries:
		form=CustRateForm(initial={'entry':entry, 'person':Person.objects.get(id=pID), 'score':1})
		forms[entry]=form
	c={}
	c['forms']=forms
	c['entries']=Entry.objects.all()
	c.update(csrf(request))
	if request.method=='POST':
		print('that was request post and here are the values:')
		personID=float(request.POST['person'])
		score=float(request.POST['score'])
		entryID=float(request.POST['entry'])
		rating=Rating(person=Person.objects.get(id=personID), score=score, entry=Entry.objects.get(id=entryID))
		rating.save()
	return render_to_response('Rate/rate_form3.html', c)
