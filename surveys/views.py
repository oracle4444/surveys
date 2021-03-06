from django.shortcuts import render, HttpResponse, get_object_or_404, get_list_or_404, Http404
from django.utils import timezone

from .models import Surveys, Questions, AnswerChoices, Users


def start_page(request):
    try:
        if not request.session.exists(request.session.session_key):
            request.session.create()
        get_object_or_404(Users, session_key=request.session.session_key)
    except Http404:
        user = Users(session_key=request.session.session_key)
        user.save()
    context = {}
    return render(request=request, template_name='surveys/start_page.html', context=context)


def surveys(request):
    try:
        surveys_list = get_list_or_404(Surveys, finish_date__gte=timezone.now())
    except Http404:
        surveys_list = []

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
    try:
        user = get_object_or_404(Users, session_key=request.session.session_key)
    except Http404:
        user = Users(session_key=request.session.session_key)
        user.save()

    questions_set = set()
    try:
        answer_choices = user.u_answers.through.objects.filter(users_id=user.id)
        answers_set = set()
        for answer_choice in answer_choices:
            answers_set.add(get_object_or_404(AnswerChoices, id=answer_choice.answerchoices_id))

        for answer in answers_set:
            questions_set.add(get_object_or_404(Questions, id=answer.question_id))
    except (Users.u_answers.through.DoesNotExist, Http404):
        ...
    questions_ids_set = set(str(question.id) for question in questions_set)
    answers_dict = {}
    last_question_id = None
    for question_id in request.POST:
        if question_id in questions_ids_set or question_id == 'csrfmiddlewaretoken':
            continue
        last_question_id = question_id

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

    try:
        survey = get_object_or_404(Surveys, id=last_question_id)
        questions = get_list_or_404(Questions, survey_id=survey.id)
        if len(questions) != 0:
            for question in questions:
                if question.type == 'multiple' and question.id not in request.POST:
                    try:
                        answer = get_object_or_404(AnswerChoices, question_id=question.id, description='')
                    except Http404:
                        answer = AnswerChoices(question_id=question.id)
                        answer.save()
                    answers_dict[question.text] = []
                    answers_dict[question.text].append(answer)
    except Http404:
        ...

    for answer_choices in answers_dict.values():
        for answer_choice in answer_choices:
            try:
                user.u_answers.through.objects.get(users_id=user.id, answerchoices_id=answer_choice.id)
            except user.u_answers.through.DoesNotExist:
                user.u_answers.through.objects.create(users_id=user.id, answerchoices_id=answer_choice.id)

    context = {'survey': survey_name, 'answers': answers_dict}
    return render(request=request, template_name='surveys/finish_survey.html', context=context)


def results_surveys(request):
    surveys_set = set()
    try:
        user = get_object_or_404(Users, session_key=request.session.session_key)
        answer_choices = user.u_answers.through.objects.filter(users_id=user.id)

        answers_set = set()
        for answer_choice in answer_choices:
            answers_set.add(get_object_or_404(AnswerChoices, id=answer_choice.answerchoices_id))

        questions_set = set()
        for answer in answers_set:
            questions_set.add(get_object_or_404(Questions, id=answer.question_id))

        for question in questions_set:
            surveys_set.add(get_object_or_404(Surveys, id=question.survey_id))
    except (Users.u_answers.through.DoesNotExist, Http404):
        ...
    context = {'surveys': surveys_set}
    return render(request=request, template_name='surveys/results_surveys.html', context=context)


def results_questions(request, survey_name):
    answers_dict = {}
    try:
        if not request.session.exists(request.session.session_key):
            request.session.create()

        user = get_object_or_404(Users, session_key=request.session.session_key)
        answer_choices = user.u_answers.through.objects.filter(users_id=user.id)

        answers_set = set()
        for answer_choice in answer_choices:
            answers_set.add(get_object_or_404(AnswerChoices, id=answer_choice.answerchoices_id))

        survey = get_object_or_404(Surveys, name=survey_name)
        questions_list = get_list_or_404(Questions, survey_id=survey.id)

        for question in questions_list:
            answers_dict[question.text] = []
            for answer in answers_set:
                if answer.question_id == question.id:
                    answers_dict[question.text].append(answer.description)

    except (Users.u_answers.through.DoesNotExist, Http404):
        ...
    context = {'answers': answers_dict}
    return render(request=request, template_name='surveys/results_questions.html', context=context)
