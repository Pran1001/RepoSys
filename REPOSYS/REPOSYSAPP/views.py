from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import StudentRegisterForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    student_form = StudentRegisterForm()
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'register.html', context)

    context = {}
    return render(request, 'register.html')

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

