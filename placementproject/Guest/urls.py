from django.urls import path,include
from Guest import views

app_name="Guest"

urlpatterns = [
    
    path('Login/',views.login,name="Login"),
    path('Userregister/',views.register,name="Userregister"),
    path('admin/',views.admin,name="admin"),
    path('logout/',views.logout,name="logout"),
    path('index/',views.index,name="index"),
]