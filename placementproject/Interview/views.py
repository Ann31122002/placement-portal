from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.http import JsonResponse
from .models import Question, InterviewResponse, inter_Question
from django.contrib import messages
from Interview.models import *
#from django.contrib.auth.decorators import login_required
import random
import json


# Create your views here.

def index(request):
    return render(request,"Interview/index.html")

def hr_interview(request):
    questions = list(Question.objects.values_list('text', flat=True))
    questions_json = json.dumps(questions)
    return render(request, 'interview/hr_interview.html', {'questions_json': questions_json})

#@login_required
def upload_response(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        video = request.FILES.get('video')
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'failed', 'error': 'User not logged in'})
        resp = InterviewResponse.objects.create(
            user=request.user,
            question_id=question_id,
            video_file=video,
            score=random.randint(60, 100),
            feedback='Auto feedback'
        )
        return JsonResponse({'status':'success', 'response_id': resp.id})
    return JsonResponse({'status':'failed'})

def view_result(request, response_id):
    response = get_object_or_404(InterviewResponse, id=response_id)
    return render(request, 'interview/result.html', {'response': response})

#@login_required
def admin_dashboard(request):
    responses = InterviewResponse.objects.select_related('user', 'question').all()
    return render(request, 'interview/admin_dashboard.html', {'responses': responses})



#@login_required
def add_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        if question_text:
            Question.objects.create(text=question_text)
            messages.success(request, "Question added successfully.")
            return redirect('Interview:manage_questions')
    return render(request, 'interview/add_question.html')


#@login_required
def manage_questions(request):
    questions = Question.objects.all()
    return render(request, 'interview/manage_questions.html', {'questions': questions})


#@login_required
def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    question.delete()
    messages.success(request, "Question deleted successfully.")
    return redirect('Interview:manage_questions')

#interview preparation questions
def addquestion(request):
    if request.method == "POST":
        q_id = request.POST.get('question_id')
        language = request.POST.get('language')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        if q_id:
            q = inter_Question.objects.get(id=q_id)
            q.language = language
            q.question = question
            q.answer = answer
            q.save()
        else:
            inter_Question.objects.create(language=language, question=question, answer=answer)

        return redirect('Interview:addquestion')  # or 'manage_questions'

    questions = inter_Question.objects.all().order_by('id')
    return render(request, 'interview/addquestion.html', {'questions': questions})

def delete_question(request, id):
    question = get_object_or_404(inter_Question, id=id)
    question.delete()
    return redirect('Interview:addquestion')

