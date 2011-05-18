from django import forms
from osp.visit.models import Visit

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
