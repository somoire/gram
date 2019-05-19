import re
from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from gram.models import Like

register = template.Library()