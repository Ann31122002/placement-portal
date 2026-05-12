from django.db import models

# Create your models here.
class tbl_userregistration(models.Model):
    user_name=models.CharField(max_length=50)
    user_contact=models.CharField(max_length=50)
    user_email=models.EmailField()
    user_gender=models.CharField(max_length=50)
    user_address=models.TextField()
    user_city=models.CharField(max_length=50)
    user_state=models.CharField(max_length=50)
    user_mark10=models.CharField(max_length=30)
    user_mark12=models.CharField(max_length=30)
    user_mark=models.CharField(max_length=30)
    user_backlog=models.CharField(max_length=30,null=True)
    user_photo=models.FileField(upload_to='Userdocs/',null=True)
    user_password=models.CharField(max_length=50)

class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.EmailField()
    admin_password=models.CharField(max_length=50)
