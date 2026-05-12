from django.db import models

# Create your models here.
class tbl_quizQtn(models.Model):
    question_text=models.TextField()
    option_a=models.CharField(max_length=50)
    option_b=models.CharField(max_length=50)
    option_c=models.CharField(max_length=50)
    option_d=models.CharField(max_length=50)
    correct_option=models.CharField(max_length=30)
    
class tbl_examtype(models.Model):
    examtype_name=models.CharField(max_length=50)


class tbl_examination(models.Model):
    examination_name=models.CharField(max_length=50) 
    examination_mark=models.CharField(max_length=50) 
    examination_qno=models.CharField(max_length=50) 
    examination_time=models.CharField(max_length=50) 
    examination_status = models.IntegerField(default=0)
    examination_date = models.DateField(null=True)
    time = models.TimeField(null=True)
    start_time = models.TimeField(null=True)
    examtype = models.ForeignKey(tbl_examtype, on_delete=models.CASCADE)

class tbl_questions(models.Model):
    question=models.CharField(max_length=100) 
    examination=models.ForeignKey(tbl_examination,on_delete=models.CASCADE)

class tbl_options(models.Model):
    questions=models.ForeignKey(tbl_questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=100)
    status = models.BooleanField() 
