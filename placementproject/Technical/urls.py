from django.urls import path
from . import views

app_name="Technical"

urlpatterns = [
    path('index/',views.index,name='index'),
    path('questions/', views.question_list, name='questions'),
    path('submit/', views.submit_code, name='submit_code'),
    path('index/', views.home, name='technical_home'),              # Serves the HTML page
    path('api/questions/', views.get_questions, name='get_questions'),
    path('api/submit/', views.submit_code, name='submit_code'),
    path('index/', views.home, name='home'),
    path('add-question/', views.add_question, name='add_question'),  # add-question page
    path('api/questions/', views.get_questions, name='get_questions'),

]


    

