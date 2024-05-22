from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth import get_user_model
from datetime import date
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from app.models import *
# from .forms import DateTimeForm


# from django.views.decorators.csrf import csrf_protect

# Create your views here.

def managerlogin(request):
    return render(request,"loginpage-manager.html")

def index(request):
    if request.user.is_anonymous:
        return render(request, 'index.html')
    else:
        if not request.user.is_staff:
            return redirect('/employee_panel')
        else:
            return redirect('/manager_panel')


def Authentication(request):
    return render(request,"Authenticate.html")


def signup_mamanger(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        eml = request.POST.get('email')
        passcode = request.POST.get('password')
        user = User.objects.create_user(uname, eml, passcode)
        # Retrieve the value of the is_staff checkbox
        is_staff = request.POST.get('is_staff')
        if is_staff:
            user.is_staff = True
            user.save()
        login(request, user)
        return redirect('/')
    else:
        pass
        return redirect("/manager")


def signup_employee(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        eml = request.POST.get('email')
        passcode = request.POST.get('password')
        uploaded_file = request.FILES['file']
        # fileobj = FileSystemStorage()
        # filepathname = fileobj.save(uploaded_file.name, uploaded_file)
        user = User.objects.create_user(uname, eml, passcode)
 
        user.save()
        
        login(request, user)
        Employeee_Pircture(file=uploaded_file,user=request.user).save()
        return redirect('employee_panel')
    else:
        return redirect('employee')


def loginuser_employee(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect('/employee_panel')

        else:
            # No backend authenticated the credentials
            return redirect('/employee')

    # return render(request, 'login_employee.html')


def loginuser_manager(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect('/manager_panel')



def logoutuser(request):
    logout(request)
    return redirect("/")


def delete(request, id):
    Todo.objects.get(pk=id).delete()
    return redirect('/manager_panel')


def get_user_instance(username_or_email):
    User = get_user_model()
    try:
        user_instance = User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        try:
            user_instance = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            user_instance = None
    return user_instance


def manager_panel(request):
    if request.user.is_anonymous:
        return redirect('/manager')
    else:
        if not request.user.is_staff:
            return HttpResponse("You are a Employee")

        else:
            user = request.user
            if request.method == 'POST':
                task = request.POST.get('task')
                date = request.POST.get('date')
                time = request.POST.get('time')
                selected_option = request.POST.get('username')
                user_instance = get_user_instance(selected_option)
                print(selected_option)
                print(request.user)
                print(time)
                var = Todo(task=task, user=user_instance, date=date, Time=time)
                var.save()
                flag = 0

            data = Todo.objects.filter()

            non_staff_users = User.objects.filter(
                is_staff=False).order_by('username')
            non_staff_usernames = [user.username for user in non_staff_users]

            return render(request, 'manager_panel.html', context={
                'var': data,
                'user_names': non_staff_usernames,
            })
        # Logic for staff users (optional)


def taskdone(request, id):
    my_instance = Todo.objects.get(pk=id)
    my_instance.status = True
    my_instance.emp_date = date.today()
    current_time = datetime.now()
    my_instance.emp_Time = current_time.time()

    my_instance.save()
    return redirect('/employee_panel')


def employee_panel(request):
    if request.user.is_anonymous:
        return redirect('/employee')
    else:
        if not request.user.is_staff:
            user_data = Todo.objects.filter(user=request.user)

            # print(user_data)
            return render(request, "employee_panel.html", {'data': user_data})
        else:
            return HttpResponse("Not account found!")


def visualization(request):
    if request.user.is_anonymous:
        return redirect('/manager')
    else:
        if not request.user.is_staff:
            return HttpResponse("You are a Employee")

        else:
            # fileobj = FileSystemStorage()
            # filepathname = fileobj.save(uploaded_file.name, uploaded_file)
            # filepathname = fileobj.url(filepathname)
            data = Todo.objects.filter()
            non_staff_users = User.objects.filter(is_staff=False)
       
    return render(request, 'Emptable.html', {'data': non_staff_users})

def count_status(subuser):
    checkbox_data = Todo.objects.filter(user=subuser)

    # Initialize counters
    true_counter=0
    false_counter=0
    # Count True and False values for each checkbox
    for data in checkbox_data:
        if data.status == True:
            true_counter+=1
        else:
            false_counter+=1
    return true_counter,false_counter
    

def subvisualization(request,username):
    subuser = User.objects.get(username=username)
    status=Todo.objects.filter(user=subuser)
    # user_images = Employeee_Pircture.objects.filter(user=subuser)
    file_obj = Employeee_Pircture.objects.get(user=subuser)  
    file_path = file_obj.file.url    
    user_data = Todo.objects.filter(user=subuser)
    
    # status count
    true,false=count_status(subuser)
    return render(request,"dashboard.html", {'user' : subuser,'status' : status,'profilepath':file_path,'task':user_data,'true':true,'false':false})

def employee(request):
    return render(request, 'employee.html')


def manager(request):
    return render(request, 'manager.html')
