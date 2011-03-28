import os

from django import forms
from django.utils import simplejson as json

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_ROOT = os.path.join(APP_ROOT, 'data')


class PersonalityTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PersonalityTypeForm, self).__init__(*args, **kwargs)

        # Get statements from JSON data file and convert to Python object
        f = file(os.path.join(DATA_ROOT, 'personality_type_statements.json'))
        data = f.read()
        data = json.loads(data)
        f.close()

        # Create fields for each statement
        #
        # Each statement is tied to a specific personality type, so name the
        # fields after the personality type. (i.e. INTP1, INTP2, etc.)
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


class LearningStyleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LearningStyleForm, self).__init__(*args, **kwargs)

        # Get statements from JSON data file and convert to Python object
        f = file(os.path.join(DATA_ROOT, 'learning_style_questions.json'))
        data = f.read()
        data = json.loads(data)
        f.close()

        # Create fields for each question
        #
        # Each question is tied to a specific learning style, so name the
        # fields after the learning style abbreviation. (i.e. K1, K2, etc.)
        i = {}
        for question in data:
            if i.has_key(question['style']):
                i[question['style']] += 1
            else:
                i[question['style']] = 1

            self.fields[question['style'] + str(i[question['style']])] = (
                forms.ChoiceField(label=question['question'], choices=(
                    ('1', 'Yes'),
                    ('0', 'No'),
                ), widget=forms.RadioSelect)
            )
