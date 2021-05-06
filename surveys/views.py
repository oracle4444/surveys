from django.shortcuts import render, HttpResponse, get_object_or_404, get_list_or_404, Http404
from django.utils import timezone

from .models import Surveys, Questions, AnswerChoices


def start_page(request):
    context = {}
    return render(request=request, template_name='surveys/start_page.html', context=context)


def surveys(request):
    try:
        surveys_list = get_list_or_404(Surveys, finish_date__gte=timezone.now())
    except Http404:
        surveys_list = []
    print(surveys_list)
    context = {'surveys': surveys_list}
    return render(request=request, template_name='surveys/surveys.html', context=context)


def questions(request, survey_name):
    try:
        survey = get_object_or_404(Surveys, name=survey_name)
        questions_list = get_list_or_404(Questions, survey_id=survey.id)
        answers_list = get_list_or_404(AnswerChoices)
    except Http404:
        questions_list = []
        answers_list = []
    context = {'survey': survey_name, 'questions': questions_list, 'answers': answers_list}
    return render(request=request, template_name='surveys/questions.html', context=context)
