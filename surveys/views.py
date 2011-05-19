from django.views.generic.simple import direct_to_template

from osp.surveys.forms import SurveyForm

def survey(request):
    form = SurveyForm()

    return direct_to_template(request, 'surveys/survey.html', {'form': form})
