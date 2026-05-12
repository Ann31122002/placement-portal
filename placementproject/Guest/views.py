from django.shortcuts import render,redirect
from Guest.models import *
from django.contrib.auth import logout
# Create your views here.

def login(request):
    if request.method=="POST":
       ucount=tbl_userregistration.objects.filter(user_email=request.POST.get('txt_email'),user_password=request.POST.get('txt_password')).count()
       acount=tbl_admin.objects.filter(admin_email=request.POST.get('txt_email'),admin_password=request.POST.get('txt_password')).count()
       if ucount>0:
        userdata=tbl_userregistration.objects.get(user_email=request.POST.get('txt_email'),user_password=request.POST.get('txt_password'))
        request.session["uid"]=userdata.id
        return redirect("Users:HomePage")
       elif acount>0:
        admindata=tbl_admin.objects.get(admin_email=request.POST.get('txt_email'),admin_password=request.POST.get('txt_password'))
        request.session["aid"]=admindata.id
        return redirect("Admin:Homepage")
       else:
           return render(request,"Guest/login.html")
    else:
       return render(request,"Guest/login.html")
       

def register(request):
    if request.method=="POST":
        tbl_userregistration.objects.create(
            user_name=request.POST.get('txt_name'),
            user_contact=request.POST.get('txt_con'),
            user_email=request.POST.get('txt_email'),
            user_gender=request.POST.get('btn_gender'),
            user_address=request.POST.get('txt_address'),
            user_city=request.POST.get('txt_city'),
            user_state=request.POST.get('txt_state'),
            user_mark10=request.POST.get('txt_mark10'),
            user_mark12=request.POST.get('txt_mark12'),
            user_mark=request.POST.get('txt_mark'),
            user_password=request.POST.get('txt_password'),
            user_photo=request.FILES.get("txt_photo"),
            user_backlog=request.POST.get('txt_backlog')
        )
        return render(request,"Guest/userregister.html")
    else:
        return render(request,"Guest/userregister.html")

def admin(request):
    if request.method=="POST":
        tbl_admin.objects.create(
            admin_name=request.POST.get('txt_name'),
            admin_email=request.POST.get('txt_email'),
            admin_password=request.POST.get('txt_password'),
            )
        return render(request,"Guest/admin.html")
    else:
        return render(request,"Guest/admin.html")

def logout(request):
    logout(request)  
    return redirect("login") 

def index(request):
    return render(request,"Guest/index.html")