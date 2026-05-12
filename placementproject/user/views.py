from Guest.models import *
from logical.models import *
from Admin.models import *
from django.db.models import Q
from datetime import time, datetime, timedelta, date
from django.http import JsonResponse
import json
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from Interview.models import *
from django.contrib import messages
#from django.contrib.auth.decorators import login_required
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import random, json



# Create your views here.


# Create your views here.
def HomePage(request):
    return render(request,"User/HomePage.html")
def Aptitude(request):
    return render(request,"User/Aptitude.html")
def Interview(request):
    return render(request,"User/Interview.html")
def Technical(request):
    return render(request,"User/Technical.html")
def interviewtips(request):
    return render(request,"User/interviewtips.html")
def looker(request):
    return render(request, "User/looker.html")
def formulas(request):
    return render(request,"User/formula.html")
def resume(request):
    return render(request,"User/resume.html")
def Aptitude_Formulas(request):
    return render(request,"User/Aptitude_Formulas.html")
def Practice_Guides(request):
    return render(request,"User/Practice_Guides.html")


def Profile(request):
    Pdata = tbl_userregistration.objects.get(id=request.session["uid"])

    return render(request,"User/Profile.html",{"Profile":Pdata})


def EditProfile(request):
    edit = tbl_userregistration.objects.get(id=request.session["uid"])
    if request.method == "POST":
        edit.user_name=request.POST.get("txt_name")
        edit.user_contact=request.POST.get("txt_con")
        edit.user_email=request.POST.get("txt_email")
        edit.user_address=request.POST.get("txt_address")
        edit.user_mark=request.POST.get("txt_mark")
        edit.user_mark10=request.POST.get("txt_mark10")
        edit.user_mark12=request.POST.get("txt_mark12")
        edit.user_state=request.POST.get("txt_state")
        edit.user_city=request.POST.get("txt_city")
        edit.user_gender=request.POST.get("txt_gender")
        edit.save()
        return redirect("Users:Profile")
    else:
        return render(request,"User/EditProfile.html",{"EditProfile":edit})


def ChangePassword(request):
    if request.method=="POST":
         ucount=tbl_userregistration.objects.filter(user_password=request.POST.get('txt_pass'),id=request.session["uid"]).count()
         if ucount>0:
             userdata=tbl_userregistration.objects.get(id=request.session["uid"])
             if request.POST.get('txt_new')==request.POST.get('txt_con'):
                userdata.user_password=request.POST.get("txt_new")
                userdata.save()
             return redirect("Users:Profile")
         else:
             return render(request,"User/ChangePassword.html")
    else:
        return render(request,"User/ChangePassword.html")


def ViewPraticeQuestion(request):
    quizqtn = tbl_quizQtn.objects.filter()
    return render(request,"User/ViewPraticeQuestion.html",{"VPratqtn":quizqtn})



def complaint(request):
    data=tbl_complaint.objects.filter(user=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get('txt_comp')
        tbl_complaint.objects.create(
            complaint_content=content,
            user=tbl_userregistration.objects.get(id=request.session['uid'])
        )
        return render(request,'User/Complaint.html',{'data':data})
    else:
        return render(request,'User/Complaint.html',{'data':data})



def notification(request):
    try:
        # 1. Fetch the logged-in user's profile data
        # Ensure the user is logged in and 'uid' is in the session
        if "uid" not in request.session:
            # Redirect to login or show an error if session is missing
            return render(request, "User/Error.html", {"message": "Please log in to view notifications."})
            
        user = tbl_userregistration.objects.get(id=request.session["uid"])
        
        # --- CRITICAL FIX: Handle None values ---
        
        # Use .get() with a default value (e.g., 0) if the attribute is None.
        # This prevents the ValueError if the user hasn't entered their data yet.
        user_mark = user.user_mark if user.user_mark is not None else 0
        user_backlog = user.user_backlog if user.user_backlog is not None else 0

        # Optional: Log or display a message if data is missing
        if user.user_mark is None or user.user_backlog is None:
             print(f"Warning: User {user.id} has missing mark/backlog data. Using defaults (Mark: 0, Backlog: 0).")
        
        # 2. Correct Filtering Logic:
        # Filter for job posts where:
        # a) The user's mark (user_mark) is >= the company's minimum mark (placement_minmark).
        #    (Therefore, company's min mark is <= user's mark)
        # b) The user's backlog (user_backlog) is <= the company's maximum allowed backlogs (placement_backlog).
        #    (Therefore, company's max backlog is >= user's backlog)
        
        jobpost = tbl_placement_drive.objects.filter(
            placement_minmark__lte=user_mark,    # User's Mark >= Company Min Mark
            placement_backlog__gte=user_backlog  # User's Backlog <= Company Max Backlogs
        ).order_by('-placement_lastdate') 
        
        return render(request, "User/Notification.html", {"notification": jobpost})

    except tbl_userregistration.DoesNotExist:
        return render(request, "User/Error.html", {"message": "User profile not found in database."})
    except Exception as e:
        # Catch any other unexpected errors and handle gracefully
        return render(request, "User/Error.html", {"message": f"An unexpected error occurred: {e}"})


def jobpost(request):
    data=tbl_placement_drive.objects.all()
    return render(request,'User/Viewjobpost.html',{'data':data})


def viewexam(request):
    user = tbl_userregistration.objects.get(id=request.session["uid"])
    exam = tbl_examination.objects.filter(examination_status__gt=0)
    for i in exam:
        exambodycount = tbl_examinationbody.objects.filter(examination=i.id,student=request.session["uid"],examinationbody_status=1).count()
        if exambodycount > 0:
            i.examstatus = 1
    return render(request,"User/ViewExam.html",{'exam':exam})

def viewquestion(request,id):
    question = tbl_questions.objects.filter(examination=id)
    optioncount = 0
    for i in question:
        count = tbl_options.objects.filter(questions=i.id).count()
        if count > 0:
            optioncount = optioncount + 1
    examcount = tbl_examinationbody.objects.filter(examination=id,user=request.session["uid"]).count()
    if examcount > 0:
        exambodyid = tbl_examinationbody.objects.get(examination=id,user=request.session["uid"])
        return render(request,"User/ViewQuestion.html",{'questions':question,"exambodyid":exambodyid.id,"optioncount":optioncount,"examination_id":id})
    else:
        exambodyid = tbl_examinationbody.objects.create(user=tbl_userregistration.objects.get(id=request.session["uid"]),examination=tbl_examination.objects.get(id=id))
        return render(request,"User/ViewQuestion.html",{'questions':question,"exambodyid":exambodyid.id,"optioncount":optioncount,"examination_id":id})

def ajaxexamanswer(request):
    exam_answer = request.GET.get('answers')
    answers_dict = json.loads(exam_answer)
    for question_key, option_id in answers_dict.items():
        questionid = question_key.split("_")[1]
        options = tbl_options.objects.get(questions=questionid,status=True)
        if option_id == None:
            tbl_examinationanswers.objects.create(examinationbody=tbl_examinationbody.objects.get(id=request.GET.get('exambodyid')),question=tbl_questions.objects.get(id=questionid),correct_answer=tbl_options.objects.get(id=options.id))
        else:
            tbl_examinationanswers.objects.create(examinationbody=tbl_examinationbody.objects.get(id=request.GET.get('exambodyid')),question=tbl_questions.objects.get(id=questionid),myanswer=tbl_options.objects.get(id=option_id),correct_answer=tbl_options.objects.get(id=options.id))
    exambody = tbl_examinationbody.objects.get(id=request.GET.get('exambodyid'))
    exambody.examinationbody_status = 1
    exambody.save()
    return JsonResponse({"msg":"Examination Submitted Sucessfully..."})

def ajaxtimer(request):
    exam = tbl_examination.objects.get(id=request.GET.get('exam'))
    timecount = tbl_timmer.objects.filter(exam=exam).count()
    if timecount > 0:
        timer_obj = tbl_timmer.objects.get(exam=exam)
        if timer_obj.timmer > time(0, 0, 0):
            current_datetime = datetime.combine(datetime.today(), timer_obj.timmer)
            new_datetime = current_datetime - timedelta(seconds=1)
            new_time = new_datetime.time()
            timer_obj.timmer = new_time
            timer_obj.save()
            time_str = new_time.strftime("%H:%M:%S")
            return JsonResponse({"msg": time_str,"status":False})
        else:
            exam.examination_status = 2
            exam.save()
            return JsonResponse({"msg": "Time's up","status":True})
    else:
        tbl_timmer.objects.create(exam=exam,timmer=exam.time)
        return JsonResponse({"msg": ""})

def successer(request):
    return render(request,"User/Success.html")


def viewresult(request, id):
    result = tbl_examinationanswers.objects.filter(examinationbody__examination=id,examinationbody__student=request.session["uid"],examinationbody__examinationbody_status=1)
    question = tbl_questions.objects.filter(examination=id).count()
    if result[0].examinationbody.total_marks == 0:
        total = 0
        for i in result:
            if i.myanswer and i.myanswer.id == i.correct_answer.id:
                total += 1
        exambody = tbl_examinationbody.objects.get(examination=id,user=request.session["uid"],examinationbody_status=1)
        exambody.total_marks = total
        exambody.save()
    return render(request,"User/ViewResult.html",{"result": result,"question":question})


def chart(request):
    return render(request, 'User/Chart.html')

def examnotification(request):
    user = tbl_userregistration.objects.get(id=request.session["uid"])
    exam = tbl_examination.objects.filter(examination_status=0)
    return render(request,"User/ExaminationNotification.html",{'exam':exam})



def hr_interview(request):
    # Make sure user is logged in
    if "uid" not in request.session:
        return redirect('Guest:login')

    # Fetch logged-in user (if needed later)
    user = tbl_userregistration.objects.get(id=request.session["uid"])

    # Prepare questions for JS
    questions_json = json.dumps([
        {'id': q.id, 'text': q.text} for q in Question.objects.all()
    ])

    return render(request, 'User/hr_interview.html', {'questions_json': questions_json})


def upload_response(request):
    if request.method == 'POST':
        if "uid" not in request.session:
            return JsonResponse({'status': 'failed', 'error': 'User not logged in'})

        user_id = request.session["uid"]
        user = get_object_or_404(tbl_userregistration, id=user_id)

        question_id = request.POST.get('question_id')
        video = request.FILES.get('video')

        if not video:
            return JsonResponse({'status': 'failed', 'error': 'No video uploaded'})

        # ✅ Create response
        resp = InterviewResponse.objects.create(
            user=user,
            question_id=question_id,
            video_file=video,
            score=random.randint(60, 100),
            feedback='Auto feedback'
        )

        return JsonResponse({'status': 'success', 'response_id': resp.id})

    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})


def view_result(request, response_id):
    if "uid" not in request.session:
        return redirect('Guest:login')

    response = get_object_or_404(InterviewResponse, id=response_id)
    return render(request, 'User/result.html', {'response': response})

def view_preparation(request):
    # Get all questions grouped by language
    questions = inter_Question.objects.all().order_by('language', 'id')
    return render(request, 'User/view_preparation.html', {'questions': questions})

def logout_user(request):
    # Check if the user is authenticated using the session key you set at login
    if "uid" in request.session:
        del request.session["uid"]  # Clear your custom user ID session variable
        # If you stored the user's name or other data, clear that too
        # del request.session["username"] 
        
    # Redirect the user to the login page or homepage (guest index)
    # Replace 'Guest:index' with the actual name of your guest homepage/login URL
    return redirect('Guest:index')


