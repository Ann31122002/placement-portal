from django.db import models
from user.models import *
from logical.models import *
from Guest.models import *
# Create your models here.
class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.CharField(max_length=50)
    admin_password=models.CharField(max_length=50)
    
class tbl_complaint(models.Model):
    complaint_content=models.CharField(max_length=50)
    date=models.DateField(auto_now_add=True)
    complaint_reply=models.CharField(max_length=50)
    status=models.IntegerField(default=0)
    user=models.ForeignKey(tbl_userregistration,on_delete=models.CASCADE)

class tbl_placement_drive(models.Model):
    placement_details=models.CharField(max_length=50)
    placement_companyname=models.CharField(max_length=50)
    placement_minmark=models.CharField(max_length=50)
    placement_backlog=models.CharField(max_length=50)
    placement_file_doc=models.FileField(upload_to="Assets/jobpost/")
    placement_lastdate=models.DateField()
    placement_status = models.IntegerField(default=0)
    user = models.ForeignKey(tbl_userregistration, on_delete=models.CASCADE,null=True)


class tbl_examinationbody(models.Model):
    examination = models.ForeignKey(tbl_examination, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(tbl_placement_drive, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(tbl_userregistration, on_delete=models.CASCADE,null=True)
    total_marks = models.IntegerField(default=0)
    examinationbody_status = models.IntegerField(default=0)


class tbl_examinationanswers(models.Model):
    examinationbody = models.ForeignKey(tbl_examinationbody, on_delete=models.CASCADE)
    question = models.ForeignKey(tbl_questions, on_delete=models.CASCADE)
    myanswer = models.ForeignKey(tbl_options, on_delete=models.CASCADE, related_name="myanswer", null=True)
    correct_answer = models.ForeignKey(tbl_options, on_delete=models.CASCADE,related_name="correct_answer")
    examinationanswers_statusq = models.IntegerField(default=0)

class tbl_timmer(models.Model):
    timmer = models.TimeField()
    exam = models.ForeignKey(tbl_examination, on_delete=models.CASCADE)
    timmer_status = models.IntegerField(default=0)