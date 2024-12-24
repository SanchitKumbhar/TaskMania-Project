from django.db import models
from datetime import date,time
from datetime import date,timedelta
from django.contrib.auth.models import User
# Create your models here.

def get_default_start_date():
    return date.today() + timedelta(days=7)  # Default to 7 days from today

class Profile(models.Model):
    photo = models.FileField(upload_to='file/')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)
    position=models.CharField(default="Employee",max_length=10)
    profilename=models.CharField(null=True,max_length=100)
    phonenumber=models.CharField(null=True,max_length=100)
    # photo=models.FileField(upload_to='file/', blank=True, null=True)



# class Todo(models.Model):
#     task = models.CharField(max_length=100)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date=models.DateField()
#     Time=models.TimeField(default=time(12, 0))
#     status = models.BooleanField(default=False)  # Default value set to True
#     emp_date=models.DateField(null=True)
#     emp_Time=models.TimeField(null=True)
#     compare_date=models.DateField(default=get_default_start_date)
#     compare_time=models.TimeField(default=time(12, 0))

#     def __str__(self):
#         return self.task

class Todo(models.Model):
    task = models.CharField(max_length=100)
    taskDesc=models.TextField(null=True,default="none")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField(default=get_default_start_date)
    status = models.BooleanField(default=False)  # Default value set to True
    emp_date=models.DateField(default=get_default_start_date)
    file = models.FileField(upload_to='documents/')

    # compare_date=models.DateField(default=get_default_start_date)

    def __str__(self):
        return self.task

