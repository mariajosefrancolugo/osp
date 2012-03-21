from django import forms
from osp.notes.models import Note
from django.conf import settings

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        exclude = ('student', 'submitter',)
