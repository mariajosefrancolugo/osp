from django import forms
from osp.visits.models import Visit
from django.conf import settings

class VisitForm(forms.ModelForm):
    reason = forms.MultipleChoiceField(choices=settings.VISIT_REASON_CHOICES)

    class Meta:
        model = Visit
        exclude = ('student', 'submitter',)

    def clean(self):
        cleaned_data=self.cleaned_data
        if cleaned_data.has_key('reason'):
            # convert reason from list to string of comma separated values
            try:
                reason_separator = settings.VISIT_REASON_SEPARATOR
            except:
                reason_separator = '; '
            reason_str = reason_separator.join(cleaned_data['reason'])
            cleaned_data['reason'] = reason_str
        return cleaned_data
