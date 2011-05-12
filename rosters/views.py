from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.core.models import Section

def roster(request, section_id):
    if not request.user.groups.filter(name='Employees'):
        raise Http403

    section = get_object_or_404(Section, id=section_id)

    if not section.instructors.filter(username=request.user.username):
        raise Http403

    return direct_to_template(request, 'rosters/roster.html',
        {'section': section})
