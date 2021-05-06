from django.urls import path

from . import views


urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('surveys/', views.surveys, name='surveys'),
    path('surveys/<str:survey_name>/', views.questions, name='questions'),
    path('surveys/<str:survey_name>/finish/', views.finish_survey, name='finish'),
    path('results_surveys/', views.results_surveys, name='results_surveys'),
]
