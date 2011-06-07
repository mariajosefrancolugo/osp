from datetime import datetime, date, time
import urllib
import xlwt
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse

from osp.core.middleware.http import Http403
from osp.assessments.models import LearningStyleResult, PersonalityTypeResult

@login_required
def learning_styles_report(request):
    if not request.user.groups.filter(name='Instructors') or not request.user.groups.filter(name='Counselors'):
        raise Http403

    if request.method == "POST":
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')
        
        results = False
        if re.match('\d{2}/\d{2}/\d{4}', from_date) and re.match('\d{2}/\d{2}/\d{4}', to_date):
            from_date = from_date.split('/')
            from_date = datetime(int(from_date[2]), int(from_date[0]), int(from_date[1]))
            to_date = to_date.split('/')
            to_date = datetime(int(to_date[2]), int(to_date[0]), int(to_date[1]))
            results = LearningStyleResult.objects.filter(date_taken__range=(datetime.combine(from_date, time.min), datetime.combine(to_date, time.max)))
        if results:
            filename = ('learning_styles-%s-%s.xls' % (from_date.strftime('%Y%m%d'), to_date.strftime('%Y%m%d')))
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Learning Styles Report')

            columns = ('User Index', 'Student Username', 'Date Taken',
                       'Learning Styles', 'Kinesthetic', 'Visual', 'Auditory')
            rows = []
            get_username = lambda x: x.username if x else "No Username"
            
            for result in results:
                row = (str(result.student.id), get_username(result.student),
                       result.date_taken.strftime('%m/%d/%Y'), result.learning_style, str(result.kinesthetic_score), 
                       str(result.visual_score), str(result.auditory_score))
                rows.append(row)
            i = 0
            for column in columns:
                ws.write(0, i, column)
                ws.col(i).width = len(column) * 255
                i += 1
            i = 1
            for row in rows:
                j = 0
                for field in row:
                    ws.write(i, j, field)
                    if ws.col(j).width < len(field) * 255:
                        ws.col(j).width = len(field) * 255
                    j += 1
                i += 1
            response = HttpResponse(mimetype="application/ms-excel")
            response['Content-Disposition'] = ('attachment; filename=%s' % filename)
            wb.save(response)
            return response
        else:
            return direct_to_template(request, 'reports/report_form.html', {'error': 'No results found for that date range.', 'learning': True, 'report_type': 'Learning Styles'})

    return direct_to_template(request, 'reports/report_form.html', {'learning': True, 'report_type': 'Learning Styles'})

def personality_type_report(request):
    if not request.user.groups.filter(name='Instructors') or not request.user.groups.filter(name='Counselors'):
        raise Http403

    if request.method == "POST":
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')
        
        if re.match('\d{2}/\d{2}/\d{4}', from_date) and re.match('\d{2}/\d{2}/\d{4}', to_date):
            from_date = from_date.split('/')
            from_date = datetime(int(from_date[2]), int(from_date[0]), int(from_date[1]))
            to_date = to_date.split('/')
            to_date = datetime(int(to_date[2]), int(to_date[0]), int(to_date[1]))
        results = PersonalityTypeResult.objects.filter(date_taken__range=(datetime.combine(from_date, time.min), datetime.combine(to_date, time.max)))
        if results:
            filename = ('personality_type-%s-%s.xls' % (from_date.strftime('%Y%m%d'), to_date.strftime('%Y%m%d')))
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Personality Type Report')

            columns = ('User Index', 'Student Username', 'Date Taken', 'Personality Type',
                       'First Category Score', 'Second Category Score', 'Third Category Score', 'Fourth Category Score')
            rows = []
            get_username = lambda x: x.username if x else "No Username"
            
            for result in results:
                row = (str(result.student.id), get_username(result.student),
                       result.date_taken.strftime('%m/%d/%Y'), result.personality_type, 
                       str(result.first_category_score), str(result.second_category_score), 
                       str(result.third_category_score), str(result.fourth_category_score),
                       )
                rows.append(row)
            i = 0
            for column in columns:
                ws.write(0, i, column)
                ws.col(i).width = len(column) * 255
                i += 1
            i = 1
            for row in rows:
                j = 0
                for field in row:
                    ws.write(i, j, field)
                    if ws.col(j).width < len(field) * 255:
                        ws.col(j).width = len(field) * 255
                    j += 1
                i += 1
            response = HttpResponse(mimetype="application/ms-excel")
            response['Content-Disposition'] = ('attachment; filename=%s' % filename)
            wb.save(response)
            return response
        else:
            return direct_to_template(request, 'reports/report_form.html', {'error': 'No results found for that date range.', 'report_type': 'Personality Type'})

    return direct_to_template(request, 'reports/report_form.html', {'report_type': 'Personality Type'})

