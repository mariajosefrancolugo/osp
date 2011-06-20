from django import forms
from django.conf import settings
from osp.interventions.models import Intervention

class InterventionForm(forms.ModelForm):
    reasons = forms.MultipleChoiceField(choices=settings.INTERVENTION_REASONS, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Intervention
        exclude = ('students', 'date_submitted', 'staff', 'section',)
