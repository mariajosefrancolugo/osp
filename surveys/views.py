import os

from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.surveys.utils import build_survey_form

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_ROOT = os.path.join(APP_ROOT, 'data')

def survey(request):
    f = file(os.path.join(DATA_ROOT, 'survey_questions.json'))
    data = f.read()
    data = json.loads(data)
    f.close()

    form = build_survey_form(data)

    return direct_to_template(request, 'surveys/survey.html', {'form': form})
