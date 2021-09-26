import csv

from django.contrib import messages, auth
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse, response
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import StudentRegisterForm, UserForm, StudentCertificateForm, StudentEducationForm, ContactForm
# Create your views here.
from .models import Student, Certificate, Education


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.user.is_superuser:
        return redirect('report')
    elif request.user.is_authenticated:
        return redirect('profile')
    else:
        form = StudentRegisterForm()
        user_form = UserForm()
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            form = StudentRegisterForm(request.POST, request.FILES)
            if user_form.errors:
                message = user_form.errors
                messages.info(request, message)
                return redirect('register')
            if form.errors:
                message = form.errors
                messages.info(request, message)
                return redirect('register')
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


def Login(request):
    if request.user.is_superuser:
        return redirect('report')
    elif request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                if user.is_superuser:
                    return redirect('report')
                else:
                    return redirect('profile')
            else:
                messages.info(request, 'Invalid Credentials !!')
                return redirect('login')

    context = {}
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')


def contact(request):
        if request.method == 'GET':
            form = ContactForm()
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                subject = form.cleaned_data['subject']
                from_email = form.cleaned_data['from_email']
                message = name + "-" + form.cleaned_data['message']
                try:
                    send_mail(subject, message, from_email, ['vstoreit@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('contactus_done')
        return render(request, "contactus.html", {'form': form})



def profile(request):
    user = request.user
    form = StudentRegisterForm(instance=user)
    context = {'form': form}
    return render(request, 'profile.html', context)


def education(request):
    form = StudentEducationForm()
    username = request.user.username
    user_obj = User.objects.get(username=username)
    if request.method == 'POST':
        form = StudentEducationForm(request.POST, request.FILES)
        if form.errors:
            message = form.errors
            messages.info(request, message)
            return redirect('education')
        if form.is_valid():
            edu_form = form.save(commit=False)
            edu_form.user = user_obj
            edu_form.save()
            return redirect('education')
    allcert = Education.objects.filter(user=user_obj)
    context = {'form': form, 'allcert': allcert}
    return render(request, 'education.html',context)


def certificates(request):
    form = StudentCertificateForm()
    username = request.user.username
    user_obj = User.objects.get(username=username)
    if request.method == 'POST':
        form = StudentCertificateForm(request.POST, request.FILES)
        if form.errors:
            message = form.errors
            messages.info(request, message)
            return redirect('certificates')
        if form.is_valid():
            cert_form = form.save(commit=False)
            cert_form.user = user_obj
            cert_form.save()
            return redirect('certificates')
    allcert = Certificate.objects.filter(user=user_obj)
    context = {'form': form, 'allcert': allcert}
    return render(request, 'certificates.html', context)



def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'vstoreit@gmail.com', [user.email])
                        return redirect("password_reset_done")
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

            else:
                messages.info(request, "User with this email Id doesn't exists")
                return redirect('password_reset')

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html",
                  context={"password_reset_form": password_reset_form})


def report(request):
    if request.user.is_superuser:
        pass
    return render(request, 'report.html')

# def export_users_csv(request):
#     response=HttpResponse(content_type='text/csv')
#     response['Content=Disposition'] = 'attachment; filename="users_csv" '
#     writer = csv.writer(response)
#     writer.writerow(['username','first_name','last_name ','email','branch'])
#
#     users = User.objects.all().values_list('username','first_name','last_name ','email','branch')
#     for user in users:
#         writer.writerow(user)
#
#     return response



def export_student_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student.csv" '
    writer = csv.writer(response)
    writer.writerow(['username','first_name','last_name ','email','branch'])

    students = Student.objects.all().values_list('username','first_name','last_name','email','branch')
    for student in students:
        writer.writerow(student)


    return response

def contactus_done(request):
    return render(request, 'Contactus_done.html')