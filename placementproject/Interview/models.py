from django.db import models
from django.contrib.auth.models import User
from Admin.models import *

class Question(models.Model):
    text = models.CharField(max_length=255)
    
    def __str__(self):
        return self.text

class InterviewResponse(models.Model):
    user = models.ForeignKey(tbl_userregistration, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    score = models.IntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}"

class inter_Question(models.Model):
    LANGUAGE_CHOICES = [
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('C++', 'C++'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('JavaScript', 'JavaScript'),
    ]
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"{self.language} - {self.question[:50]}"
