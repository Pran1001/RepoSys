from django.contrib import messages, auth
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


from .forms import StudentRegisterForm, UserForm, StudentCertificateForm
# Create your views here.
from .models import Student, Certificate




def home(request):
    return render(request, 'home.html')


def register(request, handle_uploaded_file=None):
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


def about(request):
    return render(request, 'about.html')


def profile(request):
    user = request.user
    form = StudentRegisterForm(instance=user)
    context = {'form': form}
    return render(request, 'profile.html', context)


def education(request):
    return render(request, 'education.html')


def certificates(request):
    form = StudentCertificateForm()
    if request.method == 'POST':
        form = StudentCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('certificates')
    allcert =Certificate.objects.all()
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
                        send_mail( subject, email, 'vstoreit@gmail.com', [user.email])
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
    return render(request, 'report.html')
