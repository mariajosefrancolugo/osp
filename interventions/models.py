from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

def Intervention(models.Model):
    student
    reasons
    date_submitted
    campus
    staff
    subject
    message
    
    def save(self):
        if not self.id:
            self.date_submitted = datetime.today()
            # Magical email time
        super(Intervention, self)save()
