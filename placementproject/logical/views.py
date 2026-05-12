from django.shortcuts import render,redirect
from logical.models import *
from user.models import *
from datetime import datetime

# Create your views here.
def AddpratQtn(request):
    if request.method=="POST":
        tbl_quizQtn.objects.create(
            question_text=request.POST.get('txt_question'),
            option_a=request.POST.get('txt_option_a'),
            option_b=request.POST.get('txt_option_b'),
            option_c=request.POST.get('txt_option_c'),
            option_d=request.POST.get('txt_option_d'),
            correct_option=request.POST.get('txt_correct')
        )
        return render(request,"logical/Addpratqtn.html")
    else:
        return render(request,"logical/Addpratqtn.html")

def examtype(request):
    data=tbl_examtype.objects.all()
    if request.method=="POST":
        examtype=request.POST.get('txt_exam')
        tbl_examtype.objects.create(
            examtype_name=examtype,
        )
        return render(request,'logical/Examtype.html',{'data':data})
    else:
        return render(request,'logical/Examtype.html',{'data':data})
def deletedexamtype(request,id):
    tbl_examtype.objects.get(id=id).delete()
    return redirect("Logical:examtype")
def editexamtype(request,id):
    ed=tbl_examtype.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get("txt_exam")
        ed.examtype_name=name
        ed.save()
        return redirect("Logical:examtype")
    else:
        return render(request,"logical/Examtype.html",{'edit':ed})


def examinationdetails(request):
    exm=tbl_examination.objects.filter(examination_status=0)
    examtype = tbl_examtype.objects.all()
    if  request.method=="POST":
        name=request.POST.get("txt_name")
        qno=request.POST.get("txt_qno")
        ftime = request.POST.get("txt_ftime")
        ttime = request.POST.get("txt_ttime")

        ftime_obj = datetime.strptime(ftime, "%H:%M")
        ttime_obj = datetime.strptime(ttime, "%H:%M")
        time_diff = ttime_obj - ftime_obj
        total_seconds = time_diff.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        
        time = str(hours) +" hours and "+ str(minutes) +" minutes"
        tbl_examination.objects.create(examination_name=name,examination_mark=qno,examination_qno=qno,examination_time=time,time=str(time_diff),start_time=ftime,examtype=tbl_examtype.objects.get(id=request.POST.get("sel_examtype")),examination_date=request.POST.get("txt_date"))

    return render(request,'logical/AddExamination.html',{'result':exm,"examtype":examtype})

def addquestions(request, id):
    que=tbl_questions.objects.filter(examination=id)
    if  request.method=="POST":
        examination=tbl_examination.objects.get(id=id)
        questions=request.POST.get("txt_question")
        tbl_questions.objects.create(question=questions,examination=examination)
    return render(request,'logical/Addquestion.html',{'result':que,'id':id})

def addoptions(request, id):
    que = tbl_options.objects.filter(questions=id)
    if request.method == "POST":
        questions = tbl_questions.objects.get(id=id)
        ans = request.POST.get("txt_answer")
        status = request.POST.get("txt_radio") == "True"
        count = tbl_options.objects.filter(questions=questions, status=True).count()
        if status and count > 0:
            return render(request, 'logical/Addoption.html', {
                'msg': "Corrected Answer is already added",
                'result': que,
                'id': id
            })
        else:
            tbl_options.objects.create(
                answer=ans,
                questions=questions,
                status=status
            )
            return redirect("Logical:addoptions", id=id)
    else:
        return render(request, 'logical/Addoption.html', {'result': que, 'id': id})
    
def delexm(request,id): 
    tbl_examination.objects.get(id=id).delete()
    return redirect("Logical:examinationdetails") 

def delqus(request,id,did): 
    tbl_questions.objects.get(id=id).delete()
    return redirect("Logical:addquestions",did) 

def delopt(request,id,did): 
    tbl_options.objects.get(id=id).delete()
    return redirect("Logical:addoptions",did) 

def startexam(request, id):
    exam = tbl_examination.objects.get(id=id)
    exam.examination_status = 1
    exam.save()
    return redirect("Logical:examinationdetails")

def completedexam(request):
    exm=tbl_examination.objects.filter(examination_status__gt=0)
    return render(request,"logical/CompletedExam.html",{"exam":exm})

def viewresult(request, id):
    user = tbl_userregistration.objects.filter(tbl_examinationbody__examination=id)
    return render(request, "logical/ViewResult.html", {'user': user})

def completeexam(request, id):
    exam = tbl_examination.objects.get(id=id)
    exam.examination_status = 2
    exam.save()
    return redirect("Logical:completedexam")