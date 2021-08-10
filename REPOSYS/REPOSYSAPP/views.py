from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import StudentRegisterForm, UserForm
# Create your views here.
from .models import Student


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        form = StudentRegisterForm()
        user_form = UserForm()
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            form = StudentRegisterForm(request.POST)
            if form.is_valid() and user_form.is_valid():
                username = user_form.cleaned_data.get('username')
                #            messages.success(request, f'Hi {username}, your account was created successfully')
                user_form.save()
                form.save()
                student = Student.objects.get(roll_no=username)
                student.username = User.objects.get(username=username)
                student.save()
                return redirect('login')

        context = {'form': form, 'user_form': user_form}
        return render(request, 'register.html', context)


def Login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('profile')
            else:
                messages.info(request, 'Invalid Credentials !!')
                return redirect('login')

    context = {}
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')

def about(request):
    return render(request, 'about.html')


def profile(request):
    context = {}
    return render(request, 'profile.html', context)

def education(request):
    return render(request, 'education.html')

def certificates(request):
    return render(request, 'certificates.html')

def forget(request):
    return render(request, 'forgetpass.html')


def report(request):
    return render(request, 'report.html')
