from django.urls import path,include
from logical import views
app_name="Logical"

urlpatterns = [

    path('Addpratqtn/',views.AddpratQtn,name="AddpratQtn"),
    path('examtype/',views.examtype,name="examtype"),
    path("deletedexamtype/<int:id>",views.deletedexamtype,name="deletedexamtype"),
    path("editexamtype/<int:id>",views.editexamtype,name="editexamtype"),

    path('examinationdetails/',views.examinationdetails,name='examinationdetails'),
    path('addquestions/<int:id>',views.addquestions,name='addquestions'),
    path('addoptions/<int:id>',views.addoptions,name='addoptions'),

    path('delexm/<int:id>',views.delexm,name='delexm'),
    path('delqus/<int:id>/<int:did>',views.delqus,name='delqus'),
    path('delopt/<int:id>/<int:did>',views.delopt,name='delopt'),
    path('startexam/<int:id>',views.startexam,name='startexam'),

    path('completedexam/',views.completedexam,name="completedexam"),
    path('completeexam/<int:id>',views.completeexam,name="completeexam"),
    path('viewresult/<int:id>',views.viewresult,name="viewresult"),


]