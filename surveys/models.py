from django.db import models
from django.utils import timezone


class Surveys(models.Model):
    c_name = models.CharField(max_length=200, name='name')
    c_start_date = models.DateTimeField('start date', name='start_date', null=False, default=timezone.now(), editable=False)
    c_finish_date = models.DateTimeField('finish date', name='finish_date')
    c_description = models.CharField(max_length=200, name='description')


class Questions(models.Model):
    TYPES = [
        ('text', 'question with a text answer'),
        ('single', 'question with a single choice answer'),
        ('multiple', 'question with a multiple choice answer'),
    ]
    c_survey = models.ForeignKey(Surveys, on_delete=models.CASCADE, name='survey')
    q_text = models.CharField(max_length=200, name='text')
    q_type = models.CharField(max_length=50, choices=TYPES, name='type')