from django.contrib import admin
from .models import QuizType, Question, Answer, UserResponse

@admin.register(QuizType)
class QuizTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_per_question')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz_type', 'text', 'number')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'correct')

@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_answer', 'is_correct', 'timestamp')