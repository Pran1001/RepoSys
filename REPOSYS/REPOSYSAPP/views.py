from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import StudentRegisterForm, UserForm
from django.contrib.auth.models import User


# Create your views here.
from .models import Student


def home(request):
    return render(request, 'home.html')

def register(request):
    form = StudentRegisterForm()
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        form = StudentRegisterForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            username = user_form.cleaned_data.get('username')
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

def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def forget(request):
    return render(request, 'forgetpass.html')

def report(request):
    return render(request, 'report.html')

