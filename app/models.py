from django.db import models
from datetime import date,time
from datetime import date,timedelta
from django.contrib.auth.models import User
# Create your models here.

def get_default_start_date():
    return date.today() + timedelta(days=7)  # Default to 7 days from today

class Todo(models.Model):
    task = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()
    Time=models.TimeField(default=time(12, 0))
    status = models.BooleanField(default=False)  # Default value set to True
    emp_date=models.DateField(null=True)
    emp_Time=models.TimeField(null=True)
    compare_date=models.DateField(default=get_default_start_date)
    compare_time=models.TimeField(default=time(12, 0))

    def __str__(self):
        return self.task


class Employeee_Pircture(models.Model):
    file = models.FileField(upload_to='static/file/')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)

