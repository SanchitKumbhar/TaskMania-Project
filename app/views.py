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

def position(request):
        user = Profile.objects.get(user=request.user)
        position = user.position
        print(request.user)
        if position == "Employee":
            return 0
        else:
            return 1

def index(request):
    # if request.user.is_anonymous:
    return render(request, 'index.html')
    # else:
    #     if not request.user.is_staff:
    #         return redirect('/employee_panel')
    #     else:
    #         return redirect('/manager_panel')


def Authentication(request):
    return render(request, "Authenticate.html")


def profilepage(request):
    if request.method == "POST":
        image = request.FILES.get('photo')
        profilename = request.POST.get("profilename")
        phonenumber = request.POST.get('phonenumber')
        position = request.POST.get('position')

        Profile.objects.create(profilename=profilename, phonenumber=phonenumber,
                               photo=image, user=request.user, position=position)

        if position == 'Employee':
            return redirect("/employee-panel")
        else:
            return redirect("/manager-panel")

    return render(request, "profile.html")


def signup_manager(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        eml = request.POST.get('email')
        passcode = request.POST.get('password')
        user = User.objects.create_user(uname, eml, passcode)
        user.save()
        login(request, user)
        return redirect('/')
    else:
        pass
        return redirect("/profile")


def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        Email = request.POST.get('Email')
        Password = request.POST.get('password')

        # check if user has entered correct credentials
        user = authenticate(username=username, password=Password)

        if user is not None:
            print("ok")
            # A backend authenticated the credentials
            login(request, user)
            position(request)
            return redirect("/manager-panel")
    return render(request, "login-page.html")


def signuppage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        eml = request.POST.get('email')
        passcode = request.POST.get('password')
        user = User.objects.create_user(uname, eml, passcode)
        user.save()
        login(request, user)
        return redirect('/profile')
    return render(request, "signup-page.html")


def managerloginpage(request):
    return render(request, "loginpage-manager.html")


def employeelogin(request):
    return render(request, "loginpage-employee.html")


def managerlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')

        # check if user has entered correct credentials
        user = authenticate(username=username, password=Password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect('/manager')
            # return HttpResponse("Loged in")

        # return HttpResponse("lzbfhbsdf")


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
        Profile(file=uploaded_file, user=request.user).save()
        return redirect('employee_panel')
    # else:
    #     return redirect('employee')


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
            # data = Todo.objects.filter()
            non_staff_users = User.objects.filter(is_staff=False)

    return render(request, 'Emptable.html', {'data': non_staff_users})


def count_status(subuser):
    checkbox_data = Todo.objects.filter(user=subuser)

    # Initialize counters
    true_counter = 0
    false_counter = 0
    # Count True and False values for each checkbox
    for data in checkbox_data:
        if data.status == True:
            true_counter += 1
        else:
            false_counter += 1
    return true_counter, false_counter


def subvisualization(request, username):
    subuser = User.objects.get(username=username)
    status = Todo.objects.filter(user=subuser)
    # user_images = Employeee_Pircture.objects.filter(user=subuser)
    file_obj = Profile.objects.get(user=subuser)
    file_path = file_obj.file.url
    user_data = Todo.objects.filter(user=subuser)

    # status count
    true, false = count_status(subuser)
    return render(request, "dashboard.html", {'user': subuser, 'status': status, 'profilepath': file_path, 'task': user_data, 'true': true, 'false': false})


def employee(request):
    return render(request, 'employee.html')



def manager(request):
    if request.user.is_anonymous:
        return redirect('/login-page')
    else:
        if position(request) == 1:
            if request.method == 'POST':
                    taskname = request.POST.get("taskname")
                    taskDesc = request.POST.get("taskDesc")
                    employeename = request.POST.get("employee")
                    date = request.POST.get("date")
                    user = User.objects.get(username="test")
                    empuser = Profile.objects.get(user=user)
                    Todo.objects.create(
                        task=taskname, taskDesc=taskDesc, user=empuser, date=date)
        else:
            return HttpResponse("You are a Employee")

    return render(request, 'managerpanel.html', {'emp': Profile.objects.all()})
