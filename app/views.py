import json
from datetime import datetime, date
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from app.models import *

# =========================================
# Authentication & Setup Views
# =========================================

def renderlogin(request):
    return render(request, "login-page.html")

def rendersignup(request):
    return render(request, "signup-page.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            login(request, user=user)
            # Redirect to profile creation after signup
            return redirect("/profile")
        else:
            return HttpResponse("Username already exists", status=400)
    return redirect("/signup-page")

def loginaction(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # FIX: Pass request as first arg and credentials as keyword args
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user=user)
            try:
                # FIX: Query Profile by the 'user' field, not pk
                profile = Profile.objects.get(user=user)
                if profile.position == "Employee":
                    return redirect("/employee") # Redirect to the fixed employee view
                else:
                    return redirect("/manager-panel")
            except Profile.DoesNotExist:
                # If user exists but has no profile, send them to create one
                return redirect("/profile")
        else:
            return HttpResponse("Invalid credentials", status=400)
    return redirect("/")

def logoutuser(request):
    logout(request)
    return redirect("/")

def Authentication(request):
    return render(request, "Authenticate.html")

# =========================================
# Helper Functions
# =========================================

def position(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.position == "Employee":
            return 0  # Employee
        else:
            return 1  # Manager
    except Profile.DoesNotExist:
        return -1 # No Profile

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

def organizeSort(tasknames, deadlines):
    # This function had syntax errors in original code. 
    # Commented out to prevent server crashes until you implement the sorting logic.
    pass
    # date_object = datetime.strptime(deadlines[0], "%Y-%m-%d").date()
    # dates = []
    # dates.append(date.today())
    # arrangement = []
    # for i in range(len(deadlines)): # Fixed range() syntax if you need to use this
    #     arrangement.append(dates[0]-date_object)
    # new_arrangement = sorted(arrangement)

# =========================================
# Main Logic Views
# =========================================

def index(request):
    if request.user.is_anonymous:
        return render(request, 'index.html', {})
    else:
        try:
            if Profile.objects.get(user=request.user).position == "Employee":
                return redirect('/employee')
            else:
                return redirect('/manager-panel')
        except Profile.DoesNotExist:
            return redirect('/profile')

def profilepage(request):
    if request.method == "POST":
        image = request.FILES.get('photo')
        profilename = request.POST.get("profilename")
        phonenumber = request.POST.get('phonenumber')
        position = request.POST.get('position')

        # Update or Create logic is safer here
        Profile.objects.update_or_create(
            user=request.user,
            defaults={
                'profilename': profilename,
                'phonenumber': phonenumber,
                'photo': image,
                'position': position
            }
        )

        if position == 'Employee':
            return redirect("/employee")
        else:
            return redirect("/manager-panel")

    return render(request, "profile.html")

# =========================================
# Employee Views
# =========================================

def employee(request):
    if request.user.is_anonymous:
        return redirect('/login-page')
    
    # Check if Employee
    if position(request) == 0:
        profinstance = Profile.objects.get(user=request.user)
        user_data = Todo.objects.filter(user=profinstance)

        if request.method == "POST":
            # Handle Task Updates
            task_id = request.POST.get("task")
            deadline = request.POST.get("date")
            status = request.POST.get("status")
            file = request.FILES.get("file")
            
            try:
                taskinstance = Todo.objects.get(id=task_id)
                # Ensure the task belongs to the logged-in user before updating
                if taskinstance.user == profinstance:
                    taskinstance.emp_date = deadline
                    taskinstance.status = status
                    if file:
                        taskinstance.file = file
                    taskinstance.save()
            except Todo.DoesNotExist:
                pass

        return render(request, "employeepanel.html", {'data': user_data})
    else:
        return HttpResponse("Access Denied: You are not an Employee account.")

def employee_panel(request):
    # Redirect legacy URL to the main employee view
    return redirect('/employee')

def taskdone(request, id):
    try:
        my_instance = Todo.objects.get(pk=id)
        my_instance.status = True
        my_instance.emp_date = date.today()
        my_instance.emp_Time = datetime.now().time()
        my_instance.save()
    except Todo.DoesNotExist:
        pass
    return redirect('/employee')

# =========================================
# Manager Views
# =========================================
def manager(request):
    if request.user.is_anonymous:
        return redirect('/login-page')
    
    # Check if Manager
    if position(request) == 1:
        if request.method == 'POST':
            taskname = request.POST.get("taskname")
            taskDesc = request.POST.get("taskDesc")
            employeename = request.POST.get("employee")
            date_val = request.POST.get("date")
            
            try:
                user = User.objects.get(username=employeename)
                empuser = Profile.objects.get(user=user)
                Todo.objects.create(
                    task=taskname, 
                    taskDesc=taskDesc, 
                    user=empuser, 
                    date=date_val, 
                    admin=request.user
                )
            except (User.DoesNotExist, Profile.DoesNotExist):
                return HttpResponse("Employee not found", status=404)
        
        # --- NEW CODE STARTS HERE ---
        
        # 1. Fetch employees for the dropdowns (Assign & Forward)
        emp = Profile.objects.filter(position="Employee")
        
        # 2. Fetch tasks created by this manager for the Forwarding Table
        # This populates the {% for i in data %} loop in your new modal
        tasks = Todo.objects.filter(admin=request.user) 

        context = {
            'emp': emp,
            'data': tasks  # Pass the tasks to the template
        }
        
        return render(request, 'managerpanel.html', context)
        # --- NEW CODE ENDS HERE ---

    else:
        return HttpResponse("Access Denied: You are not a Manager.")
def delete(request, id):
    try:
        Todo.objects.get(pk=id).delete()
    except Todo.DoesNotExist:
        pass
    return redirect('/manager-panel')

def visualization(request):
    if request.user.is_anonymous:
        return redirect('/manager')
    
    # Logic to show employee list table
    non_staff_users = User.objects.filter(is_staff=False)
    return render(request, 'Emptable.html', {'data': non_staff_users})

def subvisualization(request, username):
    try:
        subuser = User.objects.get(username=username)
        status = Todo.objects.filter(user=subuser)
        
        try:
            file_obj = Profile.objects.get(user=subuser)
            file_path = file_obj.file.url if file_obj.file else "" # Handle missing file
        except Profile.DoesNotExist:
            file_path = ""

        user_data = Todo.objects.filter(user=subuser)
        true_count, false_count = count_status(subuser)
        
        return render(request, "dashboard.html", {
            'user': subuser, 
            'status': status, 
            'profilepath': file_path, 
            'task': user_data, 
            'true': true_count, 
            'false': false_count
        })
    except User.DoesNotExist:
        return redirect('/manager-panel')

def count_status(subuser):
    checkbox_data = Todo.objects.filter(user=subuser)
    true_counter = 0
    false_counter = 0
    for data in checkbox_data:
        if data.status == True: # Assuming status is a boolean or string "True"
            true_counter += 1
        else:
            false_counter += 1
    return true_counter, false_counter

# def TaskForward(request):
#     data = Todo.objects.filter(admin=request.user)
#     emp = Profile.objects.filter(position="Employee")
#     return render(request, "task-forward.html", {'data': data, 'emp': emp})

# Keep this exactly as is
def forwardTaskapi(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            task_id = body.get("id")
            emp_username = body.get("emp")

            instance = Todo.objects.get(id=task_id)
            emp_user = User.objects.get(username=emp_username)
            prof_instance = Profile.objects.get(user=emp_user)
            
            instance.user = prof_instance
            instance.save()
            
            return JsonResponse({'success': "ok"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)


def allTasks(request):
    return render(request, "taskcompleted.html", {
        'data': Todo.objects.all()
    })

# =========================================
# Missing View Fix
# =========================================

def showTasksinfo(request):
    # This function was missing and causing the AttributeError.
    # It returns all tasks as JSON for API consumption.
    all_tasks = Todo.objects.all().values()
    return JsonResponse({'data': list(all_tasks)})