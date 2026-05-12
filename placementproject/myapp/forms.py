# forms.py
from django import forms
from myapp.models import QuizType, Question, Answer

class QuizSetupForm(forms.Form):
    quiz_name = forms.CharField(max_length=200, required=True, label="Quiz Name")
    num_questions = forms.IntegerField(min_value=1, max_value=50, initial=10, label="Number of Questions")
    time_per_question = forms.IntegerField(min_value=30, max_value=120, initial=60, label="Time per Question (seconds)")
    has_expiry = forms.BooleanField(required=False, label="Set Expiry Time")
    start_time = forms.DateTimeField(required=False, label="Start Time")
    end_time = forms.DateTimeField(required=False, label="End Time")

class QuestionForm(forms.Form):
    question_text = forms.CharField(widget=forms.Textarea, required=True, label="Question Text")
    option1 = forms.CharField(max_length=200, required=True, label="Option A")
    option2 = forms.CharField(max_length=200, required=True, label="Option B")
    option3 = forms.CharField(max_length=200, required=True, label="Option C")
    option4 = forms.CharField(max_length=200, required=True, label="Option D")
    correct_answers = forms.MultipleChoiceField(
        choices=[('0', 'A'), ('1', 'B'), ('2', 'C'), ('3', 'D')],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Correct Answer(s)"
    )