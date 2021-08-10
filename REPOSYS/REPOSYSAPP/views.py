from django.contrib import messages, auth
from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
from .models import Student


def home(request):
    return render(request, 'home.html')

# def register(request):
#     form = StudentRegisterForm()
#     user_form = UserForm()
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         form = StudentRegisterForm(request.POST)
#         if request.POST['password1'] == request.POST['password2']:
#             if User.objects.filter(username=request.POST['username'].exists()):
#                 messages.info(request, "User Already Exists")
#                 return redirect('register')
#             elif User.objects.filter(email=request.POST['email'].exists()):
#                 messages.info(request, "Email Already Exists")
#                 return redirect('register')
#             else:
#                 if form.is_valid() and user_form.is_valid():
#                     username = user_form.cleaned_data.get('username')
#                     user_form.save()
#                     form.save()
#                     student = Student.objects.get(roll_no=username)
#                     student.username = User.objects.get(username=username)
#                     student.save()
#                     return redirect('login')
#         else:
#             messages.info(request, "Passwords are NOT Matching")
#             return redirect('register')
#
#     context = {'form': form, 'user_form': user_form}
#     return render(request, 'register.html', context)


def register(request):
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



def profile(request):
    return render(request, 'profile.html')

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
                    messages.info(request, 'Username OR Password is incorrect')
                    return redirect('login')

    context={}
    return render(request, 'login.html', context)

def about(request):
    return render(request, 'about.html')

def forget(request):
    return render(request, 'forgetpass.html')

def report(request):
    return render(request, 'report.html')

