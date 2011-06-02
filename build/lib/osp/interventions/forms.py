from django import forms
from django.conf import settings
from osp.interventions.models import Intervention

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        exclude = ('students', 'date_submitted', 'staff', 'section',)
        widgets = {'reasons': forms.CheckboxSelectMultiple}
