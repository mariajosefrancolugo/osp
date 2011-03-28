import os

from django import forms
from django.utils import simplejson as json

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

class PersonalityTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PersonalityTypeForm, self).__init__(*args, **kwargs)

        # Get statements from JSON data file and convert to Python object
        f = file(os.path.join(os.path.join(APP_ROOT, 'data'),
            'personality_type_statements.json'))
        data = f.read()
        data = json.loads(data)
        f.close()

        i = {}
        for statement in data:
            if i.has_key(statement['type']):
                i[statement['type']] += 1
            else:
                i[statement['type']] = 1

            self.fields[statement['type'] + str(i[statement['type']])] = (
                forms.ChoiceField(label=statement['statement'], choices=(
                    ('2', 'Strongly Agree'),
                    ('1', 'Agree'),
                    ('-1', 'Disagree'),
                    ('-2', 'Strongly Disagree'),
                ), widget=forms.RadioSelect)
            )
