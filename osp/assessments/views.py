import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.assessments.forms import PersonalityTypeForm, LearningStyleForm, AssessmentForm
from osp.assessments.lib import jungian
from osp.assessments.models import PersonalityTypeResult, LearningStyleResult
from osp.assessments.utils import load_json_data
from osp.core.middleware.http import Http403

class Assessment(object):
    """
        Class for creating custom assessments.
    """
    def __init__(self, request, result_model, title="Assessment", data_root=""):
        if not request.user.groups.filter(name__in=['Students', 'Employees']):
            raise Http403
        self.result_model = result_model
        self.title = title
        self.data_root = data_root

    def show(self, request, form_class=AssessmentForm, template="custom_assessments/assessment.html"):
        if request.method == 'POST':
            form = form_class(request.POST, data_root=self.data_root)
            if form.is_valid():
                # Save form data.
                result = self.save_assessment(request, form)
                # Redirect to results page
                return self.outcome(request, result.pk)
        else:
            form = form_class(data_root=self.data_root)
        return direct_to_template(request, template,
            {'form': form,
             'title': self.title})

    def save_assessment(self, request, form):
        """
           Save the student's responses to the questions.
        """
        answers = []
        for item in form.cleaned_data:
            if item in form.fields:
                answers.append({'question':form.fields[item].label,
                                'answer':form.cleaned_data[item],
                                'question_id':item})
                
        answers = json.dumps(answers)
        # Save results
        result = self.result_model(
            student=request.user,
            answers=answers,
        )
        result.save()
        return result

    def score(self, request, result_id):
        """
            Score the student's responses to the assessment. This is primarily
            provided as an example, but it works for questions that have one
            specific correct answer.
        """
        questions = load_json_data('assessment.json', self.data_root)
        answers = self.get_responses(request, result_id)
        correct = []
        incorrect = []
        unanswered = []
        for question in questions:
            if 'question_id' in question and 'correct_answer' in question and 'question' in question:
                if question['question_id'] in answers:
                    question_id = question['question_id']
                    answer = answers[question_id]
                    if answer['answer'] == question['correct_answer']:
                        correct.append(question['question_id'])
                    else:
                        if answer['answer'] == '':
                            unanswered.append(question['question_id'])
                        else:
                            incorrect.append(question['question_id'])
        return correct, incorrect, unanswered

    def outcome(self, request, result_id):
        """
            Display the outcome of the assessment based on the student's
            responses to the questions and subsequent scoring.
        """
        result = self.result_model.objects.get(pk=result_id)
        correct, incorrect, unanswered = self.score(request, result_id)

        descriptions = [{"description":"testing testing. this is a custom test."}]
        return direct_to_template(request, 'custom_assessments/assessment_results.html',
            {'result': result,
             'title': self.title,
             'descriptions': descriptions,
             'correct': correct,
             'incorrect':incorrect,
             'unanswered':unanswered})

    def get_questions(self, request):
        questions = load_json_data('assessment.json', self.data_root)
        return questions

    def get_responses(self, request, result_id):
        """
            Returns responses provided by the student to each question.
        """
        result = self.result_model.objects.get(pk=result_id)
        responses = {}
        answers = json.loads(result.answers)
        for answer in answers:
            responses[answer['question_id']] = {'question':answer['question'], 'answer':answer['answer']}
        return responses

    def show_responses(self, request, result_id):
        """
            Displays the student's responses to the questions.
        """
        responses = self.get_responses(request, result_id)
        questions = self.get_questions(request)
        # Build a dictionary of responses to display.  This will ensure they are in the
        # same order as the questions presented on the assessment.
        responses_to_display = []
        for question in questions:
            if 'question_id' in question:
                question_id = question['question_id']
                if question_id in responses:
                    responses_to_display.append(responses[question_id])
        return direct_to_template(request, 'custom_assessments/assessment_responses.html',
            {'responses':responses_to_display,
             'title':self.title})


@login_required
def personality_type(request):
    if not request.user.groups.filter(name__in=['Students', 'Employees']):
        raise Http403

    if request.method == 'POST':
        form = PersonalityTypeForm(request.POST)
        if form.is_valid():
            # Use the Jungian library to analyze the results of the assessment
            analysis = jungian.TypeAnalysis(form.cleaned_data, 4, 100)

            # Extract important pieces of data from the analysis
            answers = json.dumps(form.cleaned_data)
            personality_type= ''.join(map(lambda x: x[0],
                analysis.computedScores))
            first, second, third, fourth = map(lambda x: x[1],
                analysis.computedScores)

            # Save results
            result = PersonalityTypeResult(
                student=request.user,
                answers=answers,
                personality_type=personality_type,
                first_category_score=first,
                second_category_score=second,
                third_category_score=third,
                fourth_category_score=fourth
            )
            result.save()

            # Redirect to results page
            return redirect('assessment:personality-type-results',
                result_id=result.pk)
    else:
        form = PersonalityTypeForm()

    return direct_to_template(request, 'assessments/personality_type.html',
        {'form': form})

@login_required
def personality_type_results(request, result_id):
    if not request.user.groups.filter(name__in=['Students', 'Employees']):
        raise Http403

    # Get personality type test results
    result = PersonalityTypeResult.objects.get(pk=result_id)

    # Make sure the logged-in user should have access to these results
    if (not request.user.groups.filter(name='Employees') and
        result.student != request.user):
        raise Http403

    # Get description of personality type from JSON data
    description = load_json_data(os.path.join('personality_types',
        '%s.json' % result.personality_type.lower()))

    if request.is_ajax():
        template = 'assessments/personality_type_results_ajax.html'
    else:
        template = 'assessments/personality_type_results.html'

    return direct_to_template(request, template,
        {'result': result, 'description': description})

@login_required
def learning_style(request):
    if not request.user.groups.filter(name__in=['Students', 'Employees']):
        raise Http403

    if request.method == 'POST':
        form = LearningStyleForm(request.POST)
        if form.is_valid():
            # Caluluate totals
            form_data = form.cleaned_data
            kin = sum([int(i) for k, i in form_data.items() if k[:3] == 'kin'])
            aud = sum([int(i) for k, i in form_data.items() if k[:3] == 'aud'])
            vis = sum([int(i) for k, i in form_data.items() if k[:3] == 'vis'])

            # Convert answers to JSON
            answers = json.dumps(form_data)

            # Determine style(s)
            styles = []
            if kin >= aud and kin >= vis:
                styles.append('kinesthetic')
            if vis >= aud and vis >= kin:
                styles.append('visual')
            if aud >= kin and aud >= vis:
                styles.append('auditory')
            styles = ', '.join(styles)

            # Save results
            result = LearningStyleResult(
                student=request.user,
                answers=answers,
                learning_style=styles,
                kinesthetic_score=kin,
                visual_score=vis,
                auditory_score=aud
            )
            result.save()

            # Redirect to results page
            return redirect('assessment:learning-style-results',
                result_id=result.pk)
    else:
        form = LearningStyleForm()

    return direct_to_template(request, 'assessments/learning_style.html',
        {'form': form})

@login_required
def learning_style_results(request, result_id):
    if not request.user.groups.filter(name__in=['Students', 'Employees']):
        raise Http403

    # Get learning style test results
    result = LearningStyleResult.objects.get(pk=result_id)

    # Make sure the logged-in user should have access to these results
    if (not request.user.groups.filter(name='Employees') and
        result.student != request.user):
        raise Http403

    # Get description of learning style(s) from JSON data
    descriptions = []
    for style in result.learning_style.split(', '):
        descriptions.append(load_json_data(os.path.join('learning_styles',
            '%s.json' % style.lower())))

    if request.is_ajax():
        template = 'assessments/learning_style_results_ajax.html'
    else:
        template = 'assessments/learning_style_results.html'

    return direct_to_template(request, template,
        {'result': result, 'descriptions': descriptions})
