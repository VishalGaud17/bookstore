from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'authapp/signup.html')



def login_view(request):

    print("Username:", username)
    print("Password:", password)
    print("Authenticated User:", user)

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # or wherever you want
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'authapp/login.html')


def custom_logout(request):
    logout(request)
    return redirect('login')


def test_login(request):
    u = authenticate(username="admin", password="admin123")
    return HttpResponse(f"User: {u}")


# Create your views here.

