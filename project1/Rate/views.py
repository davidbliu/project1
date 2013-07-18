from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person, Comment, Saved
from Rate.helpers import *
import decimal
import time
from decimal import *
from image_size import *
from django import forms
from datetime import datetime
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory

def activity_view(request, personID=1):
	message='this is activity view for '
	person=Person.objects.get(id=personID)
	me=None
	if request.user.is_authenticated():
		me=Person.objects.filter(user=request.user)[0]
	print 'my friends are'
	friends= person.friends.all()
	comments=Comment.objects.filter(person=person)
	ratings=Rating.objects.filter(person=person)
	uploads=Entry.objects.filter(added_by=person)

	if request.method=='POST':
		if request.POST.get('add_friend') is not None:
			print 'so you want to add this friend'
			if request.user.is_authenticated:
				me=Person.objects.get(user=request.user)
				me.friends.add(person)
				me.save()
		if request.POST.get('delete_friend') is not None:
			print 'so you want to delete this friend'
			if request.user.is_authenticated:
				# me=Person.objects.get(user=request.user)
				# fil= me.friends.filter(person)
				# fil.delete()
				print me.friends.remove(person)

	args={}
	args.update(csrf(request))
	# args['friend_with_me']=None
	if person in me.friends.all():
		args['friends_with_me']='klsjdfljslkdjf'
		print 'yes we are friends'
	args['message']=message
	args['main_person']=person
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	args['request']=request
	args['comments']=comments.order_by('updated').reverse()
	args['friends']=friends
	args['ratings']=ratings.order_by('updated').reverse()
	args['uploads']=uploads.order_by('date_added').reverse()
	args['entries']=Entry.objects.all()
	args['comment_dict']=get_top_comment_dict(args['entries'])
	args['portfolio']=Saved.objects.filter(person=args['main_person'])
	args['recent_messages']=get_recent_messages(args['person'], 5)
	return render_to_response('Rate/activity_view.html', args)
def cat_list(request, which=0):
	which=float(which)
	cList=Category.objects.all()
	handle_delete_button(request)
	handle_save_button(request)
	if request.method=='POST':
		if request.POST.get('cat_name') != None:
			print request.POST.get('cat_name')
			category=Category(type=request.POST.get('cat_name'))
			category.save()
			return HttpResponseRedirect('.')
		if request.POST.get('search_cats') != None:
			print(request.POST.get('search_cats'))
			cList=filter_cats_by_term(request.POST.get('search_cats'))
	args={}
	args.update(csrf(request))
	args['categories']=cList
	args['request']=request
	args['entries']=Entry.objects.all()
	if which==1:
		print 'i am here'
		args['entries']=Entry.objects.all().order_by('score').reverse()
		print args['entries']
		for e in args['entries']:
			print e.score
	if which==2:
		args['entries']=Entry.objects.all().order_by('date_added').reverse()
	if which==3:
		v=get_friends_activities(Person.objects.filter(user=request.user)[0])
		args['activities']=v
	if which==4:
		person=Person.objects.filter(user=request.user)
		if person is not None:
			args['entries']=Entry.objects.filter(added_by=person).order_by('date_added').reverse()
		else:
			args['entries']=None
	if which==5:
		person=Person.objects.filter(user=request.user)[0]
		if person is not None:
			args['activities']=get_my_rates(person)
			args['onlyme']=1
		else:
			args['activities']=None
			args['onlyme']=None
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	args['comment_dict']=get_top_comment_dict(args['entries'])
	args['portfolio']=Saved.objects.filter(person=args['person'])
	args['recent_messages']=get_recent_messages(args['person'], 5)
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
	args['comment_dict']=get_top_comment_dict(args['entries'])
	args['portfolio']=Saved.objects.filter(person=args['person'])
	args['recent_messages']=get_recent_messages(args['person'], 5)
	return render_to_response('Rate/entry_by_category.html', args)

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
		if 'add_portfolio' in request.POST:
			if request.user.is_authenticated():
				person=Person.objects.get(user=request.user)
				existing=Saved.objects.filter(person=person, entry=entry)
				if len(existing) ==0:
					s=Saved(person=person, entry=entry)
					s.save()
		if 'delete_entry' in request.POST:
			entry.delete()
			return HttpResponseRedirect('/categories')
		if 'edit_entry' in request.POST:
			return HttpResponseRedirect('/upload/entry/%s' % entry.id)
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
		if 'add_comment' in request.POST:
			comment_text=request.POST.get('comment_text')
			comment=Comment(person=Person.objects.get(user=request.user), comment=comment_text, entry=entry)
			comment.save()
		return HttpResponseRedirect('.')
		print ("a post request was made while examining entry"+ comment_text)
	args={}
	args.update(csrf(request))
	args['entries']=Entry.objects.all()
	args['entry']=entry
	args['score']=score
	args['rates']=Rating.objects.filter(entry=entry)
	args['comments']=comments.order_by('updated').reverse()
	args['request']=request
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	args['comment_dict']=get_top_comment_dict(args['entries'])
	args['portfolio']=Saved.objects.filter(person=args['person'])
	args['recent_messages']=get_recent_messages(args['person'], 5)
	return render_to_response('Rate/entry_detail.html', args)
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
	args['comment_dict']=get_top_comment_dict(args['entries'])
	args['portfolio']=Saved.objects.filter(person=args['person'])
	return render_to_response('Rate/friends.html', args)

def like_comment_view(request, likeID=-1, cID=1, pID=1):
	com=Comment.objects.get(id=cID)
	entry=com.entry
	if likeID=='1':
		string=com.likers
		mylist=string.split(',')
		if pID not in mylist:
			com.likers+=pID 
			com.likers+=','
			com.likes+=1
			com.score=com.likes-decimal.Decimal(.75)*com.dislikes
			com.save()
	elif likeID=='2':
		string=com.dislikers
		mylist=string.split(',')
		if pID not in mylist:
			print com.dislikers
			com.dislikers+=pID
			com.dislikers+=','
			com.dislikes+=1
			com.score=com.likes-decimal.Decimal(.75)*com.dislikes
			com.save()
	return HttpResponseRedirect('/entry/%s' % entry.id)

def people_view(request):
	people_list=Person.objects.all()
	if request.method=='POST':
		if request.POST.get('search_people') != None:
			people_list=filter_people_by_term(request.POST.get('search_people'))
	args={}
	args.update(csrf(request))
	args['people']=people_list
	args['entries']=None
	args['request']=request
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	args['portfolio']=Saved.objects.filter(person=args['person'])
	args['recent_messages']=get_recent_messages(args['person'], 5)
	return render_to_response('Rate/people.html',args)
class AvatarForm(forms.Form):
	avatar=forms.URLField()
def settings_view(request):
	message='welcome'
	form=AvatarForm()
	my_person=None
	if request.user.is_authenticated():
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
	args['comment_dict']=get_top_comment_dict(args['entries'])
	args['portfolio']=Saved.objects.filter(person=args['person'])
	return render_to_response('Rate/settings.html', args)
class EntryForm(ModelForm):
	class Meta:
		model=Entry
		fields=['name','category','image','description','added_by']
		widgets={
			'added_by':forms.HiddenInput(),
		}
def upload_view(request, cID=-1, eID=-1):
	message='you need to log in to upload a new image' 
	eID=float(eID)
	instance=None
	eForm=EntryForm(instance=instance)
	if(request.user.is_authenticated()):
		eForm=EntryForm(initial={'added_by':Person.objects.filter(user=request.user)[0]})
		if cID!=-1:
			eForm=EntryForm(initial={'category':Category.objects.filter(id=cID)[0],'added_by':Person.objects.filter(user=request.user)[0]})
		if eID !=-1:
			instance=Entry.objects.get(id=eID)
			eForm=EntryForm(instance=instance)
		message='welcome '
		message+=request.user.username
		message+=' please provide image link'
	if request.method=='POST':
		if request.user.is_authenticated():
			eForm=EntryForm(request.POST.copy(), instance=instance)
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
	args['comment_dict']=get_top_comment_dict(args['entries'])
	args['portfolio']=Saved.objects.filter(person=args['person'])
	return render_to_response('Rate/upload.html', args)



# print 'testing the helpers thing............................'
# 	l=[]
# 	l.append('lwekrj')
# 	bob='keyword,34'
# 	l.append(bob)
# 	key='keyword'
# 	if(decipher(key,l)):
# 		print 'success'
# 		print decipher(key,l)
# 	print 'done testign the helpers thing......................'