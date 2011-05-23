from django.contrib.auth.models import User
from django.db import models


class Result(models.Model):
    student = models.ForeignKey(User)
    date_taken = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    result = models.ForeignKey(Result)
    question = models.TextField()
    answer = models.CharField(max_length=255)
