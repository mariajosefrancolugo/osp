from django.db import models


class AssessmentResult(models.Model):
    answers = models.TextField()
    personality_type = models.CharField(max_length=255)
    first_category_score = models.IntegerField()
    second_category_score = models.IntegerField()
    third_category_score = models.IntegerField()
    fourth_category_score = models.IntegerField()
