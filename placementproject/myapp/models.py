# models.py
from django.db import models
from django.contrib.auth.models import User

class QuizType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    time_per_question = models.IntegerField(default=60)
    has_expiry = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE)
    text = models.TextField()
    number = models.IntegerField()

    def __str__(self):
        return f"{self.quiz_type.name} - Q{self.number}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question} - {self.text}"
        
class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Response"
        verbose_name_plural = "User Responses"

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:20]}"

class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE)
    attempted = models.BooleanField(default=False)
    attempt_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quiz_type')