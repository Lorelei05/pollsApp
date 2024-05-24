from django.urls import path
from . import views

app_name = 'poll'
urlpatterns = [
    #localhost:8000/poll/
    path('', views.home, name='home'),
    #localhost:8000/poll/vote/
    path('<int:q_id>/vote/', views.vote, name='vote'),
    #localhost:8000/poll/result/
    path('<int:q_id>/result/', views.result, name='result')
]