from django import template
from Rate.models import Person
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.assignment_tag()
def person_from_user(user):
	person=Person.objects.get(user=user)
	return person
@register.assignment_tag()
def resolve(d, key):
    try:
        return d.get(key)
    except:
        return None
@register.assignment_tag()
def order_assign(mylist, attribute):
	print 'here is list'
	print mylist
	print 'here si attribute'
	print attribute
	# return sorted(mylist, key='added')
	newlist = sorted(mylist, key=lambda x: x.added, reverse=True)
	return newlist
	
@register.simple_tag()
def order(mylist, attribute):
	return mylist.order_by(attribute)

# {% resolve some_list some_index as value %}
# {% resolve some_dict some_dict_key as value %}