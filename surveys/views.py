from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.surveys.forms import SurveyForm

@login_required
def survey(request):
    if not request.user.groups.filter(name='Students'):
        raise Http403

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            print form.fields['question_1'].label
            return redirect('profile:profile', request.user.id)
    else:
        form = SurveyForm()

    return direct_to_template(request, 'surveys/survey.html', {'form': form})
