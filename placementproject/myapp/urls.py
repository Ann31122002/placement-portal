# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.quiz_dashboard, name='quiz_dashboard'),  # Root of myapp.urls
    path('setup/', views.quiz_setup, name='quiz_setup'),
    path('add-question/', views.add_question, name='add_question'),
    path('add-question/<int:quiz_type_id>/', views.add_question, name='add_question_for_quiz'),
    path('<int:quiz_type_id>/', views.take_quiz, name='take_quiz'),
    path('<int:quiz_type_id>/results/', views.quiz_results, name='quiz_results'),
    path('quiztypes/', views.quiztype_list, name='quiztype_list'),
    path('quiztypes/<int:quiz_type_id>/edit-questions/', views.edit_questions, name='edit_questions'),
    path('quiztypes/<int:quiz_type_id>/questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('quiztypes/<int:quiz_type_id>/questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('analytics/', views.analytics, name='analytics'),
    path('home/', views.HomePage, name='home'),
    path('adminhome/', views.HomePage2, name='adminhome'),
]