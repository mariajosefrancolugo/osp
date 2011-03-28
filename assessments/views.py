from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.assessments.forms import PersonalityTypeForm, LearningStyleForm
from osp.assessments.lib import jungian
from osp.assessments.models import PersonalityTypeResult, LearningStyleResult

def personality_type(request):
    if request.method == 'POST':
        form = PersonalityTypeForm(request.POST)
        if form.is_valid():
            # Use the Jungian library to analyze the results of the assessment
            analization = jungian.TypeAnalysis(form.cleaned_data, 4, 100)

            # Extract important pieces of data from the analysis
            answers = json.dumps(form.cleaned_data)
            personality_type= ''.join(map(lambda x: x[0],
                analization.computedScores))
            first, second, third, fourth = map(lambda x: x[1],
                analization.computedScores)
    else:
        form = PersonalityTypeForm()
    return direct_to_template(request, 'assessments/personality_type.html',
        {'form': form})

def personality_type_results(request):
    pass

def learning_style(request):
    form = LearningStyleForm()
    return direct_to_template(request, 'assessments/learning_style.html',
        {'form': form})

def learning_style_results(request):
    pass
