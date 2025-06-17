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
    if authenticate(request.POST.get("username"),request.POST.get("password")) is not None:
        login(request,authenticate(request.POST.get("username"),request.POST.get("password")))
        profile = Profile.objects.get(pk=request.user)
        if profile.position == "Employee":
            return redirect("/employee-panel")
        else:
            return redirect("/manager-panel")
    
    return HttpResponse("Bad Request")

def logoutuser(request):
    logout(request)
    return redirect("/")