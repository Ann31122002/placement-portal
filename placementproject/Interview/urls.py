# from django.urls import path,include
# from Interview import views
# from . import views
# app_name="Interview"

# urlpatterns = [
#    path('Index/',views.index,name="index"),

#    path('hr/', views.hr_interview, name='hr_interview'),
#    path('upload/', views.upload_response, name='upload_response'),
#    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
   
#    path('add-question/', views.add_question, name='add_question'),
#    path('manage-questions/', views.manage_questions, name='manage_questions'),
#    path('delete-question/<int:id>/', views.delete_question, name='delete_question'),

# ]
from django.urls import path
from . import views

app_name = 'Interview'  # ✅ Must match the include namespace if you use one

urlpatterns = [
   #  path('hr/', views.hr_interview, name='hr_interview'),
   #  path('upload/', views.upload_response, name='upload_response'),    
   #  path('result/<int:response_id>/', views.view_result, name='view_result'),

    # ✅ admin side URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-question/', views.add_question, name='add_question'),
    path('manage-questions/', views.manage_questions, name='manage_questions'),
    path('delete-question/<int:id>/', views.delete_question, name='delete_question'),
    
    path('addquestion/', views.addquestion, name='addquestion'),
    path('delete/<int:id>/', views.delete_question, name='delete_question'),
]
