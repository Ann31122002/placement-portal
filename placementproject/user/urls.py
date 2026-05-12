from django.urls import path,include
from user import views
from django.conf.urls.static import static
# 💡 IMPORT QUIZ VIEWS: Import the views file from your quiz application (e.g., 'myapp')
from myapp import views as quiz_views

app_name="Users"

urlpatterns = [

    path('HomePage/',views.HomePage,name="HomePage"),
    path('Aptitude/',views.Aptitude,name="Aptitude"),
    path('Practice_Guides/',views.Practice_Guides,name="Practice_Guides"),
    path('Aptitude_Formulas/',views.Aptitude_Formulas,name="Aptitude_Formulas"),
    path('Interview/',views.Interview,name="Interview"),
    path('interviewtips/',views.interviewtips,name="interviewtips"),
    path('formulas/',views.formulas,name="formulas"),
    path('resume/',views.resume,name="resume"),
    path('Technical',views.Technical,name="Technical"),
    path('looker/', views.looker, name='looker'),

    path('Profile/',views.Profile,name="Profile"),
    path('EditProfile/',views.EditProfile,name="EditProfile"),
    path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
    path('ViewPraticeQuestion/',views.ViewPraticeQuestion,name="ViewPraticeQuestion"),

    path('notification/',views.notification,name="notification"),
    path('Complaint/',views.complaint,name="complaint"),
    path('Viewjobpost/',views.jobpost,name="viewjobpost"),

    path('viewexam/',views.viewexam,name='viewexam'),
    path('viewquestion/<int:id>',views.viewquestion,name='viewquestion'),
    path('ajaxexamanswer/',views.ajaxexamanswer,name='ajaxexamanswer'),
    path('ajaxtimer/',views.ajaxtimer,name='ajaxtimer'),
    path('successer/',views.successer,name='successer'),

    path('viewresult/<int:id>',views.viewresult,name='viewresult'),

    path('chart/',views.chart,name='chart'),
   

    path('notification/',views.notification,name="notification"),
    path('examnotification/',views.examnotification,name="examnotification"),

    
    path('hr/', views.hr_interview, name='hr_interview'),
    path('upload/', views.upload_response, name='upload_response'),    
    path('result/<int:response_id>/', views.view_result, name='view_result'),

    
    path('view_preparation/', views.view_preparation, name='view_preparation'),
    path('logout/', views.logout_user, name="Logout"),

    # 1. View all available quizzes for the user to select one
    path('quiz/list/', quiz_views.quiztype_list, name='quiz_list'),
    
    # 2. Start/Continue taking a specific quiz
    path('quiz/<int:quiz_type_id>/take/', quiz_views.take_quiz, name='take_quiz_user'),
    
    # 3. View results for the completed quiz
    path('quiz/<int:quiz_type_id>/results/', quiz_views.quiz_results, name='quiz_results_user'),
]