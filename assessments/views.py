from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.assessments import forms, models

def personality_type(request):
    form = forms.PersonalityTypeForm()
    return direct_to_template(request, 'assessments/personality_type.html',
        {'form': form})

def personality_type_results(request):
    pass

def learning_style(request):
    pass

def learning_style_results(request):
    pass
