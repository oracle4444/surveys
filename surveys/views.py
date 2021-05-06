from django.shortcuts import render, HttpResponse, get_object_or_404, get_list_or_404, Http404
from django.utils import timezone

from .models import Surveys


def start_page(request):
    context = {}
    return render(request=request, template_name='surveys/start_page.html', context=context)


def surveys(request):
    try:
        surveys_list = get_list_or_404(Surveys, finish_date__gte=timezone.now())
    except Http404:
        surveys_list = []
    context = {'surveys': surveys_list}
    return render(request=request, template_name='surveys/surveys.html', context=context)