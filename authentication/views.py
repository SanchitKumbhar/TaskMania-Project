from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from app.models import Profile

def renderlogin(request):
    return render(request,"login-page.html")

def rendersignup(request):
    return render(request,"signup-page.html")

def signup(request):
    user=User.objects.create_user(request.POST.get("username"),request.POST.get("email"),request.POST.get("password"))
    login(request,user=user)
    return redirect("/profile")

def loginaction(request):
    # Get data from the form
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    # FIX 1: Pass credentials as KEYWORD arguments (username=..., password=...)
    # Also pass 'request' as the first argument.
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user=user)
        try:
            # FIX 2: Query using 'user=user' instead of 'pk=user.id'
            # This assumes your Profile model has a OneToOneField to User named 'user'
            profile = Profile.objects.get(user=user)
            
            if profile.position == "Employee":
                return redirect("/employee")
            else:
                return redirect("/manager-panel")
                
        except Profile.DoesNotExist:
            # FIX 3: If user exists but Profile is missing, redirect them to create it
            # instead of showing an error.
            return redirect("/profile")
            
    return HttpResponse("Invalid credentials", status=400)
def logoutuser(request):
    logout(request)
    return redirect("/")