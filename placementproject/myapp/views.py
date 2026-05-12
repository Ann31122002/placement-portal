from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import QuizType, Question, Answer, UserResponse, UserQuizAttempt
from myapp.forms import QuizSetupForm, QuestionForm
from django.contrib import messages
from django.http import Http404, HttpResponse
from io import StringIO
import logging
import csv
from datetime import datetime
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver    
from django.core.management import call_command  # ← NEW!
from django.db import transaction

logger = logging.getLogger(__name__)

def quiz_dashboard(request):
    quiz_types = QuizType.objects.annotate(num_questions=Count('question')).filter(num_questions__gt=0)
    logger.debug(f"Quiz types retrieved for dashboard: {list(quiz_types.values('id', 'name'))}")
    if not quiz_types:
        messages.info(request, "No quizzes available. Please create one.")
    print("Rendering quiz_dashboard")
    return render(request, 'quiz/questdashboard.html', {'quiz_types': quiz_types})

def quiz_setup(request):
    if request.method == 'POST':
        setup_form = QuizSetupForm(request.POST)
        if setup_form.is_valid():
            quiz_name = setup_form.cleaned_data['quiz_name']
            num_questions = setup_form.cleaned_data['num_questions']
            time_per_question = setup_form.cleaned_data['time_per_question']
            
            quiz_type, created = QuizType.objects.get_or_create(name=quiz_name)
            quiz_type.time_per_question = time_per_question
            quiz_type.save()
            
            request.session['quiz_setup'] = {
                'quiz_type_id': quiz_type.id,
                'num_questions': num_questions,
                'time_per_question': time_per_question,
                'current_question': 1
            }
            logger.debug(f"Quiz setup saved: {request.session['quiz_setup']}")
            return redirect('add_question')
    else:
        setup_form = QuizSetupForm()
    return render(request, 'quiz/register.html', {'setup_form': setup_form})

def add_question(request, quiz_type_id=None):
    quiz_setup = request.session.get('quiz_setup')
    if not quiz_setup and not quiz_type_id:
        messages.error(request, "Please select a quiz to add questions to.")
        return redirect('quiz_dashboard')
    
    if quiz_type_id:
        quiz_type = get_object_or_404(QuizType, id=quiz_type_id)
        existing_questions = Question.objects.filter(quiz_type=quiz_type).count()
        quiz_setup = {
            'quiz_type_id': quiz_type.id,
            'num_questions': 50,  # ← FIXED: UNLIMITED (was existing_questions + 1)
            'time_per_question': quiz_type.time_per_question or 60,
            'current_question': existing_questions + 1
        }
        request.session['quiz_setup'] = quiz_setup
        request.session.modified = True
    
    quiz_type = QuizType.objects.get(id=quiz_setup['quiz_type_id'])
    current_question = quiz_setup['current_question']
    num_questions = quiz_setup['num_questions']  # ← FIXED: Use 50, not existing + 1

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            try:
                with transaction.atomic():
                    question = Question.objects.create(
                        quiz_type=quiz_type,
                        text=question_form.cleaned_data['question_text'],
                        number=current_question
                    )
                    
                    options = [
                        question_form.cleaned_data['option1'],
                        question_form.cleaned_data['option2'],
                        question_form.cleaned_data['option3'],
                        question_form.cleaned_data['option4']
                    ]
                    correct_indices = [int(i) for i in question_form.cleaned_data['correct_answers']]
                    
                    for i, option_text in enumerate(options):
                        Answer.objects.create(
                            question=question,
                            text=option_text,
                            correct=i in correct_indices
                        )
                
                # UPDATE SESSION - FIXED!
                quiz_setup['current_question'] += 1
                request.session['quiz_setup'] = quiz_setup
                request.session.modified = True
                
                messages.success(request, f"✅ Question {current_question} added! ({quiz_setup['current_question']-1}/{num_questions})")
                
                # ← FIXED: ALWAYS CONTINUE (no limit check)
                return redirect('add_question_for_quiz', quiz_type_id=quiz_type.id)
                
            except Exception as e:
                logger.error(f"Error: {e}")
                messages.error(request, f"Failed to save: {str(e)}")
    else:
        question_form = QuestionForm()
    
    return render(request, 'quiz/register.html', {
        'question_form': question_form,
        'current_question': current_question,
        'num_questions': num_questions,
        'quiz_name': quiz_type.name
    })

    
def quiztype_list(request):
    quiz_types = QuizType.objects.annotate(num_questions=Count('question')).filter(num_questions__gt=0)
    logger.debug(f"Quiz types retrieved: {list(quiz_types.values('id', 'name'))}")
    if not quiz_types:
        messages.info(request, "No quizzes available. Please create one.")
    return render(request, 'quiz/quiztype_list.html', {'quiz_types': quiz_types})


def take_quiz(request, quiz_type_id=None):
    if not quiz_type_id:
        quiz_types = QuizType.objects.annotate(num_questions=Count('question')).filter(num_questions__gt=0)
        if not quiz_types:
            messages.warning(request, "No quizzes available. Please create one.")
            return redirect('quiz_dashboard')
        return render(request, 'quiz/user_quiz_horizontal.html', {
            'quiz_types': quiz_types
        })

    try:
        quiz_type = QuizType.objects.get(id=quiz_type_id)
        logger.debug(f"Accessing quiz_type_id: {quiz_type_id}, name: {quiz_type.name}")
        questions = Question.objects.filter(quiz_type=quiz_type).order_by('number')
        if not questions:
            messages.warning(request, f"No questions available for '{quiz_type.name}'. Please add questions first.")
            return redirect('quiz_dashboard')
        
        # Check expiry
        current_time = timezone.now()
        if quiz_type.has_expiry:
            if quiz_type.end_time and current_time > quiz_type.end_time:
                quiz_type.delete()
                messages.error(request, f"The quiz '{quiz_type.name}' has expired and was deleted.")
                return redirect('quiz_dashboard')
            if quiz_type.start_time and current_time < quiz_type.start_time:
                messages.error(request, f"The quiz '{quiz_type.name}' starts at {quiz_type.start_time}.")
                return redirect('quiz_dashboard')

        # Initialize or retrieve session state
        session_key = f"quiz_{quiz_type_id}_state"
        if session_key not in request.session:
            request.session[session_key] = {
                'current_question': 0,
                'user_answers': {},
                'bookmarks': {},
                'time_left': {},
                'quiz_type_id': quiz_type_id
            }
        quiz_state = request.session.get(session_key, {})
        current_question_index = quiz_state.get('current_question', 0)

        if request.method == 'POST':
            action = request.POST.get('action', 'next')
            selected_answer_id = request.POST.get('answer')
            bookmark_checked = request.POST.get('bookmark', 'off') == 'on'
            time_left_post = request.POST.get('time_left', str(quiz_type.time_per_question))

            try:
                time_left_post = int(time_left_post)
            except ValueError:
                time_left_post = quiz_type.time_per_question

            if selected_answer_id:
                question = questions[current_question_index]
                selected_answer = Answer.objects.get(id=selected_answer_id)
                quiz_state['user_answers'][str(question.id)] = selected_answer_id
                # Create guest user if not authenticated
                if not request.user.is_authenticated:
                    from django.contrib.auth.models import User
                    session_id = request.session.session_key or 'anonymous'
                    if not session_id:
                        request.session.save()
                        session_id = request.session.session_key
                    username = f"guest_{session_id[:8]}"
                    user_obj, _ = User.objects.get_or_create(
                        username=username,
                        defaults={'email': f"{username}@quiz.com", 'is_active': False}
                    )
                else:
                    user_obj = request.user
                UserResponse.objects.create(
                    user=user_obj,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=selected_answer.correct
                )

            quiz_state['bookmarks'][str(current_question_index)] = bookmark_checked
            quiz_state['time_left'][str(current_question_index)] = time_left_post
            request.session[session_key] = quiz_state
            request.session.modified = True

            logger.debug(f"POST action: {action}, user_answers: {quiz_state['user_answers']}")

            if action == 'nav':
                new_index = int(request.POST.get('target_question', str(current_question_index)))
                quiz_state['current_question'] = new_index if 0 <= new_index < len(questions) else current_question_index
            elif action == 'previous' and current_question_index > 0:
                quiz_state['current_question'] = current_question_index - 1
            elif action in ['skip', 'next', 'save_and_next'] and current_question_index < len(questions) - 1:
                quiz_state['current_question'] = current_question_index + 1
            elif action == 'submit':
                quiz_state['current_question'] = len(questions)

            request.session[session_key] = quiz_state
            request.session.modified = True

            if quiz_state['current_question'] >= len(questions):
                return redirect('quiz_results', quiz_type_id=quiz_type_id)
            return redirect(reverse('take_quiz', args=[quiz_type_id]))

        if current_question_index >= len(questions):
            return redirect('quiz_results', quiz_type_id=quiz_type_id)
        
        current_question = questions[current_question_index]
        answers = current_question.answer_set.all()
        time_left_value = quiz_state['time_left'].get(str(current_question_index), quiz_type.time_per_question)
        is_bookmarked = quiz_state['bookmarks'].get(str(current_question_index), False)
        user_answers = quiz_state.get('user_answers', {})
        bookmarks = quiz_state.get('bookmarks', {})

        return render(request, 'quiz/user_quiz_horizontal.html', {
            'quiz_type': quiz_type,
            'question': current_question,
            'answers': answers,
            'current_question_number': current_question_index + 1,
            'total_questions': len(questions),
            'time_per_question': quiz_type.time_per_question,
            'is_bookmarked': is_bookmarked,
            'time_left_value': str(time_left_value),
            'user_answers': user_answers,
            'bookmarks': bookmarks,
            'questions': questions
        })
    except QuizType.DoesNotExist:
        logger.error(f"QuizType with id {quiz_type_id} does not exist")
        raise Http404("Quiz type does not exist")

def quiz_results(request, quiz_type_id):
    try:
        quiz_type = QuizType.objects.get(id=quiz_type_id)
        questions = Question.objects.filter(quiz_type=quiz_type).order_by('number')
        
        # Determine user (guest or authenticated)
        if request.user.is_authenticated:
            user_obj = request.user
        else:
            from django.contrib.auth.models import User
            session_id = request.session.session_key or 'anonymous'
            if not session_id:
                request.session.save()
                session_id = request.session.session_key
            username = f"guest_{session_id[:8]}"
            user_obj, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': f"{username}@quiz.com", 'is_active': False}
            )

        # GET USER ANSWERS FROM DATABASE
        user_responses = UserResponse.objects.filter(
            user=user_obj,
            question__quiz_type=quiz_type
        ).select_related('question', 'selected_answer').order_by('question__number')
        
        # **FIXED SCORING - WORKS 100%**
        score = 0
        detailed_results = []
        
        # LOOP THROUGH ALL QUESTIONS
        for question in questions:
            # FIND USER'S ANSWER FOR THIS QUESTION
            user_response = user_responses.filter(question=question).first()
            
            if user_response and user_response.selected_answer:
                # USER ANSWERED
                is_correct = user_response.is_correct
                selected_answer = user_response.selected_answer
                if is_correct:
                    score += 1
            else:
                # NO ANSWER OR SKIPPED
                is_correct = False
                selected_answer = None
            
            detailed_results.append({
                'question': question,
                'selected_answer': selected_answer,
                'is_correct': is_correct
            })
        
        total_questions = len(questions)
        
        # **AUTO UPDATE SHEETS**
        call_command('export_responses', format='sheets')
        
        # **CLEAN SESSION**
        session_key = f"quiz_{quiz_type_id}_state"
        if session_key in request.session:
            del request.session[session_key]
            request.session.modified = True
        
        # **SHOW SUCCESS**
        messages.success(request, f'🎉 Quiz completed! Score: {score}/{total_questions}')
        messages.info(request, '📊 Data sent to Google Sheets!')
        
        print(f"*** QUIZ RESULTS *** Score: {score}/{total_questions}")
        print(f"*** Detailed: {len(detailed_results)} results")
        
        return render(request, 'quiz/quiz_results.html', {
            'quiz_type': quiz_type,
            'score': score,
            'total_questions': total_questions,
            'detailed_results': detailed_results
        })
        
    except QuizType.DoesNotExist:
        messages.error(request, "Quiz not found!")
        return redirect('quiz_dashboard')

        
def edit_questions(request, quiz_type_id):
    quiz_type = get_object_or_404(QuizType, id=quiz_type_id)
    questions = Question.objects.filter(quiz_type=quiz_type).order_by('number')
    if not questions.exists():
        messages.warning(request, f"No questions available for '{quiz_type.name}'. Consider adding some.")
        return redirect('quiz_dashboard')
    return render(request, 'quiz/edit_questions.html', {
        'quiz_type': quiz_type,
        'questions': questions
    })

def edit_question(request, quiz_type_id, question_id):
    quiz_type = get_object_or_404(QuizType, id=quiz_type_id)
    question = get_object_or_404(Question, id=question_id, quiz_type=quiz_type)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            try:
                with transaction.atomic():
                    question.text = question_form.cleaned_data['question_text']
                    question.save()
                    question.answer_set.all().delete()
                    options = [
                        question_form.cleaned_data['option1'],
                        question_form.cleaned_data['option2'],
                        question_form.cleaned_data['option3'],
                        question_form.cleaned_data['option4']
                    ]
                    correct_indices = [int(i) for i in question_form.cleaned_data['correct_answers']]
                    if any(i >= len(options) for i in correct_indices):
                        raise ValueError("Correct answer index exceeds available options")
                    for i, option_text in enumerate(options):
                        Answer.objects.create(
                            question=question,
                            text=option_text,
                            correct=i in correct_indices
                        )
                    logger.debug(f"Question {question.id} updated with new answers")
                    messages.success(request, 'Question updated successfully.')
                    return redirect('edit_questions', quiz_type_id=quiz_type_id)
            except Exception as e:
                logger.error(f"Error updating question {question_id}: {str(e)}")
                messages.error(request, f"Failed to update question: {str(e)}")
    else:
        answers = question.answer_set.all()
        initial_data = {
            'question_text': question.text,
            'option1': answers[0].text if answers and len(answers) > 0 else '',
            'option2': answers[1].text if answers and len(answers) > 1 else '',
            'option3': answers[2].text if answers and len(answers) > 2 else '',
            'option4': answers[3].text if answers and len(answers) > 3 else '',
            'correct_answers': [str(i) for i, ans in enumerate(answers) if ans.correct] if answers else []
        }
        question_form = QuestionForm(initial=initial_data)
    return render(request, 'quiz/edit_question.html', {
        'quiz_type': quiz_type,
        'question': question,
        'question_form': question_form
    })

def delete_question(request, quiz_type_id, question_id):
    quiz_type = get_object_or_404(QuizType, id=quiz_type_id)
    question = get_object_or_404(Question, id=question_id, quiz_type=quiz_type)
    if request.method == 'POST':
        question_number = question.number
        question.delete()
        questions = Question.objects.filter(quiz_type=quiz_type).order_by('number')
        for i, q in enumerate(questions, 1):
            q.number = i
            q.save()
        logger.debug(f"Question {question_id} deleted, renumbered questions for quiz {quiz_type_id}")
        messages.success(request, 'Question deleted successfully.')
        if not Question.objects.filter(quiz_type=quiz_type).exists():
            quiz_type.delete()
            messages.info(request, f"Quiz '{quiz_type.name}' removed as it has no questions.")
        return redirect('quiz_dashboard')
    return render(request, 'quiz/confirm_delete.html', {'question': question, 'quiz_type': quiz_type})

def export_responses(request):
    responses = UserResponse.objects.all().select_related('user', 'question__quiz_type', 'selected_answer')

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'User', 'User_Email', 'Quiz_Type', 'Quiz_Start_Time', 'Quiz_End_Time', 'Question_Number', 'Question_Text', 'Selected_Answer', 'Correct_Answers', 'Is_Correct', 'Response_Timestamp'
    ])

    for response in responses:
        correct_answers = ', '.join([a.text for a in response.question.answer_set.filter(correct=True)])
        quiz_start = response.question.quiz_type.start_time.isoformat() if response.question.quiz_type.start_time else ''
        quiz_end = response.question.quiz_type.end_time.isoformat() if response.question.quiz_type.end_time else ''
        writer.writerow([
            response.user.username,
            response.user.email,
            response.question.quiz_type.name,
            quiz_start,
            quiz_end,
            str(response.question.number),
            response.question.text.replace('\n', ' '),
            response.selected_answer.text,
            correct_answers,
            '1' if response.is_correct else '0',
            response.timestamp.isoformat()
        ])

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'user_responses_{timestamp}.csv'
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
# ... ALL YOUR VIEWS ...

@receiver(post_save, sender=UserResponse)
def auto_export(sender, instance, created, **kwargs):
    if created:
        call_command('export_responses')

def analytics(request):
    """Render Looker Studio dashboard"""
    return render(request, 'quiz/analytics.html')

def HomePage(request):
    return render(request,"User/HomePage.html")

def HomePage2(request):
    return render(request,"Admin/HomePage.html")