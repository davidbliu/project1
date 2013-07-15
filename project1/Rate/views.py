from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person, Comment
from django import forms
from datetime import datetime
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory

def activity_view(request, personID=1):
	message='this is activity view for '
	person=Person.objects.get(id=personID)
	print 'my friends are'
	friends= person.friends.all()
	comments=Comment.objects.filter(person=person)
	ratings=Rating.objects.filter(person=person)
	uploads=Entry.objects.filter(added_by=person)
	args={}
	args['message']=message
	args['main_person']=person
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	args['request']=request
	args['comments']=comments
	args['friends']=friends
	args['ratings']=ratings
	args['uploads']=uploads
	args['entries']=Entry.objects.all()
	return render_to_response('Rate/activity_view.html', args)
def cat_list(request):
	# activity_list=get_activities(Person.objects.filter(user=request.user)[0])
	# print activity_list
	# print 'that was the act list'
	cList=Category.objects.all()
	if request.method=='POST':
		category=Category(type=request.POST.get('cat_name'))
		category.save()
		return HttpResponseRedirect('.')
	args={}
	args.update(csrf(request))
	args['recent_activities']=get_activities(Person.objects.filter(user=request.user)[0])
	args['categories']=cList
	args['request']=request
	args['entries']=Entry.objects.all()
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('Rate/category_list.html',args)
def entry_by_category_list(request, cID='1'):
	cat=Category.objects.get(id=cID)
	entryList=Entry.objects.filter(category=cat)
	if request.method=='POST':
		if 'delete_category' in request.POST:
			cat.delete()
			return HttpResponseRedirect('/categories')
	args={}
	args.update(csrf(request))
	args['category']=cat
	args['entryList']=entryList
	args['request']=request
	args['entries']=entryList
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('Rate/entry_by_category.html', args)


def friends_view(request):
	message='these are your friends:'
	print request.user
	print 'is about to view friends'
	friends=[]
	try:
		person = Person.objects.get(user=request.user)
		friends=person.friends.all()
		print person.friends.all()
	except:
		message='your person does not exist'
	args={}
	args.update(csrf(request))
	args['entries']=Entry.objects.all()
	args['request']=request
	args['message']=message
	args['friends']=friends
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('Rate/friends.html', args)

def entry_detail(request, eID='0', opts=()):
	entry=get_object_or_404(Entry, pk=eID)
	ratings=Rating.objects.all()
	score=0
	numRates=0
	for rate in ratings:
		if rate.entry==entry:
			score+=rate.score
			numRates+=1
	if (numRates !=0 ):
		score=score/numRates
		entry.score=score
		entry.save()
	comments=Comment.objects.filter(entry=entry)
	if request.method=='POST':
		if 'delete_entry' in request.POST:
			entry.delete()
			return HttpResponseRedirect('/categories')
		if 'rate' in request.POST:
			if request.user.is_authenticated():
				p=Person.objects.filter(user=request.user)[0]
				myRates=Rating.objects.filter(person=p)
				for r in myRates:
					if r.entry==entry:
						r.delete()
						# each person can only rate the item once, so replaces all old ratings
			rate=Rating(entry=entry, person=Person.objects.get(user=request.user), score=float(request.POST['rate']))
			rate.save()
		else:
			print 'rate was not in the post thingymajigx'
		if 'add_comment' in request.POST:
			comment_text=request.POST.get('comment_text')
			comment=Comment(person=Person.objects.get(user=request.user), comment=comment_text, entry=entry)
			comment.save()
		else:
			print 'add comment was not in request post thing'
		return HttpResponseRedirect('.')
		print ("a post request was made while examining entry"+ comment_text)
	args={}
	args.update(csrf(request))
	args['entries']=Entry.objects.all()
	args['entry']=entry
	args['score']=score
	args['comments']=comments
	args['request']=request
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('Rate/entry_detail.html', args)
class AvatarForm(forms.Form):
	avatar=forms.URLField()
def settings_view(request):
	message='welcome'
	form=AvatarForm()
	my_person=Person.objects.filter(user=request.user)[0]
	friends=[]
	if my_person:
		friends=my_person.friends.all()
	if request.method=='POST':
		if request.POST['submit']=='change avatar' and request.user.is_authenticated():
			p=Person.objects.filter(user=request.user)[0]
			if p:
				p.avatar=request.POST['avatar']
				p.save()
				message='sucessfully changed avatar'
				return HttpResponseRedirect('.')
			else:
				print 'failed'
	args={}
	args.update(csrf(request))
	args['entries']=Entry.objects.all()
	args['form']=form
	args['message']=message
	args['request']=request
	args['friends']=friends
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('Rate/settings.html', args)
class EntryForm(ModelForm):
	class Meta:
		model=Entry
def upload_view(request, cID=-1):
	message='you need to log in to upload a new image' 
	eForm=EntryForm()
	if(request.user.is_authenticated()):
		eForm=EntryForm(initial={'added_by':Person.objects.filter(user=request.user)[0]})
		if cID!=-1:
			eForm=EntryForm(initial={'category':Category.objects.filter(id=cID)[0],'added_by':Person.objects.filter(user=request.user)[0]})
		message='welcome '
		message+=request.user.username
		message+=' please provide image link'
	if request.method=='POST':
		if request.user.is_authenticated():
			eForm=EntryForm(request.POST.copy())
			if eForm.is_valid():
				message='Thank you for submitting your image'
				eForm.save()
				return HttpResponseRedirect('/categories')
			else:
				message='not a valid form'
		else:
			message='you must be logged in to submit a new image sorry'
	args={}
	args.update(csrf(request))
	args['entries']=Entry.objects.all()
	args['message']=message
	args['request']=request
	args['eForm']=eForm
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('Rate/upload.html', args)

def get_activities(person):
	friends=person.friends.all()
	ans=[]
	for rate in Rating.objects.all():
		if rate.person in friends:
			ans.append(rate)
	for entry in Entry.objects.all():
		if entry.added_by in friends:
			ans.append(entry)
	for comment in Comment.objects.all():
		if comment.person in friends:
			ans.append(comment)
	return ans