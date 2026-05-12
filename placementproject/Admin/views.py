from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from logical.models import *
from django.db.models import Q
# 💡 REQUIRED IMPORTS for jobpost email functionality
from django.core.mail import send_mail
from django.conf import settings


def HomePage(request):
    return render(request,"Admin/HomePage.html")
 


def jobpost(request):
    data = tbl_placement_drive.objects.filter(placement_status=1)
    if request.method == "POST":
        companyname = request.POST.get('txt_companyname')
        details = request.POST.get('txt_details')
        mincgpa = float(request.POST.get('txt_mincgpa'))
        backlog = request.POST.get('txtback')  
        file_doc = request.FILES.get('file_doc')
        lastdate = request.POST.get('txt_lastdate')
        job = tbl_placement_drive.objects.create(
            placement_companyname=companyname,
            placement_details=details,
            placement_minmark=mincgpa,
            placement_backlog=backlog,
            placement_file_doc=file_doc,
            placement_lastdate=lastdate,
            placement_status=1
        )

        # Get eligible students (CGPA >= mincgpa and no backlogs)
        eligible_students = tbl_userregistration.objects.filter(
            user_mark=mincgpa,  # Greater than or equal to min CGPA
            user_backlog= backlog ,# Assuming '0' means no backlogs
        )
        
        # Prepare email content
        subject = f'New Job Opportunity at {companyname}'
        message = (
            "Dear Student,\n\n"
            f"A new job opportunity has been posted that matches your profile:\n\n"
            f"Company: {companyname}\n"
            f"Details: {details}\n"
            f"Minimum CGPA Required: {mincgpa}\n"
            f"Backlog Limit: {backlog}\n"
            f"Last Date to Apply: {lastdate}\n\n"
            "Please check the attached document (if any) and apply before the deadline.\n"
            "For more details, login to your student portal.\n\n"
            "Best Regards,\n"
            "Placement Training and preparation portal"
        )
        
        # Send email to all eligible students
        for user in eligible_students:
            email=user.user_email
            # print(email)
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
        
        return render(request, 'Admin/JobPost.html',{'data':data})
    else:
        return render(request, 'Admin/JobPost.html',{'data':data})



def deletedjobpost(request,id):
    tbl_placement_drive.objects.get(id=id).delete()
    return redirect("Admin:jobpost")

def eligiblelist(request,id):
    data=tbl_placement_drive.objects.get(id=id)
    user=tbl_userregistration.objects.filter(user_mark=data.placement_minmark,user_backlog=data.placement_backlog)
    # print(student)
    return render(request,'Admin/Eligiblelist.html',{'user':user,'company':data})

def viewcomplaint(request):
    data=tbl_complaint.objects.filter(status=0)
    replied=tbl_complaint.objects.filter(status=1)
    return render(request,'Admin/Viewcomplaint.html',{'data':data,'replied':replied})

def reply(request,id):
    data=tbl_complaint.objects.get(id=id)
    if request.method=="POST":
        reply=request.POST.get('txt_reply')
        data.complaint_reply=reply
        data.status=1
        data.save()
        return redirect("Admin:viewcomplaint")
    else:
        return render(request,'Admin/Reply.html')