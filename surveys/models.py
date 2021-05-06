from django.db import models
from django.utils import timezone


class Surveys(models.Model):
    c_name = models.CharField(max_length=200, name='name')
    c_start_date = models.DateTimeField('start date', name='start_date', null=False, default=timezone.now(), editable=False)
    c_finish_date = models.DateTimeField('finish date', name='finish_date')
    c_description = models.CharField(max_length=200, name='description')

    def __str__(self):
        return self.name


class Questions(models.Model):
    TYPES = [
        ('text', 'question with a text answer'),
        ('single', 'question with a single choice answer'),
        ('multiple', 'question with a multiple choice answer'),
    ]
    c_survey = models.ForeignKey(Surveys, on_delete=models.CASCADE, name='survey')
    q_text = models.CharField(max_length=200, name='text')
    q_type = models.CharField(max_length=50, choices=TYPES, name='type')


class AnswerChoices(models.Model):
    a_question = models.ForeignKey(Questions, on_delete=models.CASCADE, name='question')
    a_description = models.CharField(max_length=200, default='', name='description')


class Users(models.Model):
    u_session_key = models.CharField(max_length=32, name='session_key', null=False)
    u_answers = models.ManyToManyField(AnswerChoices)
