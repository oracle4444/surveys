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


def finish_survey(request, survey_name):
    answers_dict = {}
    for question_id in request.POST:
        if question_id == 'csrfmiddlewaretoken':
            continue

        question = get_object_or_404(Questions, id=question_id)
        answers_dict[question.text] = []

        if question.type == 'text':
            answer_choice = AnswerChoices(description=request.POST[question_id], question_id=question.id)
            answer_choice.save()
            answers_dict[question.text].append(answer_choice)
        elif question.type == 'single':
            answer_choice = AnswerChoices.objects.get(id=int(request.POST[question_id]))
            answers_dict[question.text].append(answer_choice)
        else:
            for ans in request.POST.getlist(question_id):
                answer_choice = AnswerChoices.objects.get(id=int(ans))
                answers_dict[question.text].append(answer_choice)

    context = {'survey': survey_name, 'answers': answers_dict}
    return render(request=request, template_name='surveys/finish_survey.html', context=context)
