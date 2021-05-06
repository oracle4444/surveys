from django.shortcuts import render, HttpResponse


def start_page(request):
    context = {}
    return render(request=request, template_name='surveys/start_page.html', context=context)
