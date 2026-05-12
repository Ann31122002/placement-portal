
import sqlite3
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Question, Submission
from .serializers import QuestionSerializer, SubmissionSerializer
from django.shortcuts import render,redirect

@api_view(['GET'])
def question_list(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def submit_code(request):
    serializer = SubmissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(status='Received')
        return Response({'message':'Submission received successfully!'})
    return Response({'message':'Invalid submission data'}, status=400)

def index(request):
    return render(request,"Technical/index.html")


# Renders your HTML page
def home(request):
    return render(request, 'technical/index.html')


# API endpoint for fetching all questions
@api_view(['GET'])
def get_questions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


# API endpoint for submitting code
@api_view(['POST'])
def submit_code(request):
    serializer = SubmissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(result="Received")
        return Response({'message': 'Submission received successfully!'})
    return Response({'message': 'Invalid data!'}, status=400)


@api_view(['POST'])
def submit_code(request):
    try:
        question_id = request.data.get('question_id')
        language = request.data.get('language')
        code = request.data.get('code')

        if not all([question_id, language, code]):
            return Response({'message': 'Missing required fields'}, status=400)

        question = Question.objects.filter(id=question_id).first()
        if not question:
            return Response({'message': 'Question not found'}, status=404)

        submission = Submission.objects.create(
            question=question,
            language=language,
            code=code,
            result="Received"
        )
        submission.save()

        return Response({'message': 'Submission stored successfully!'}, status=201)

    except Exception as e:
        print("Error:", e)
        return Response({'message': 'Server error'}, status=500)
    

# Existing home (index.html)
def home(request):
    return render(request, 'technical/index.html')

# 🆕 Add question page (renders + handles form)
def add_question(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        difficulty = request.POST.get('difficulty')

        Question.objects.create(
            title=title,
            description=description,
            difficulty=difficulty
        )
        return redirect('/')  # Redirect back to main page after adding
    return render(request, 'technical/add_question.html')


# API for questions
@api_view(['GET'])
def get_questions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


# API for submissions
@api_view(['POST'])
def submit_code(request):
    try:
        question_id = request.data.get('question_id')
        language = request.data.get('language')
        code = request.data.get('code')

        if not all([question_id, language, code]):
            return Response({'message': 'Missing required fields'}, status=400)

        question = Question.objects.filter(id=question_id).first()
        if not question:
            return Response({'message': 'Question not found'}, status=404)

        Submission.objects.create(
            question=question,
            language=language,
            code=code,
            result="Received"
        )
        return Response({'message': 'Submission stored successfully!'}, status=201)

    except Exception as e:
        print(e)
        return Response({'message': 'Server error'}, status=500)


@api_view(['POST'])
def submit_code(request):
    try:
        question_id = request.data.get('question_id')
        language = request.data.get('language')
        code = request.data.get('code')

        if not all([question_id, language, code]):
            return Response({'message': 'Missing required fields'}, status=400)

        question = Question.objects.filter(id=question_id).first()
        if not question:
            return Response({'message': 'Question not found'}, status=404)

        # ---- retry loop in case database is temporarily locked ----
        for _ in range(5):
            try:
                Submission.objects.create(
                    question=question,
                    language=language,
                    code=code,
                    result="Received"
                )
                connection.close()
                return Response({'message': 'Submission stored successfully!'}, status=201)
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    import time
                    time.sleep(1)   # wait 1 s and retry
                    continue
                raise e
        return Response({'message': 'Database busy, try again later.'}, status=503)
        # -----------------------------------------------------------

    except Exception as e:
        print("🔥 ERROR:", e)
        return Response({'message': 'Server error'}, status=500)



