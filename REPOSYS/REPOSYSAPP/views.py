import csv

from django.contrib import messages, auth
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import *
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
    return render(request, 'education.html', context)


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


def generate_full_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vstoreit_all_students_report.csv" '
    writer = csv.writer(response)

    writer.writerow(['PROFILE DETAILS'])
    writer.writerow([])
    writer.writerow(
        ['USERID', 'FIRST NAME', 'LASTNAME', 'ROLL NO', 'EMAIL', 'ADDMISSION DATE', 'YEAR', 'BRANCH', 'DIV', 'MOBILE'])
    students = Student.objects.all().values_list('username', 'first_name', 'last_name', 'roll_no', 'email',
                                                 'date_of_add', 'year',
                                                 'branch', 'div', 'mobile')
    for student in students:
        writer.writerow(student)
    writer.writerow([])
    writer.writerow([])

    writer.writerow(['EDUCATION DETAILS'])
    writer.writerow([])
    writer.writerow(
        ['USERID', 'QUALIFICATION LEVEL', 'COUNTRY', 'STATE', 'DISTRICT', 'COLLEGE NAME', 'ADDMISSION YEAR', 'STREAM',
         'COURSE NAME',
         'RESULT', 'PASS YEAR', 'COMPLETED', 'PERCENTAGE', 'BOARD/UNIVERSITY NAME', 'MODE', 'ATTEMPTS TAKEN',
         'MARKSHEET'])
    educations = Education.objects.all().values_list('user', 'qua_level', 'country', 'state', 'district',
                                                     'college_name', 'admission_year', 'stream', 'course_name',
                                                     'result', 'pass_year', 'completed', 'percentage',
                                                     'board_university', 'mode', 'attempts', 'upload_marksheet')
    for education in educations:
        writer.writerow(education)
    writer.writerow([])
    writer.writerow([])

    writer.writerow(['CERTIFICATE DETAILS'])
    writer.writerow([])
    writer.writerow(
        ['USERID', 'TYPE OF CERTIFICATE', 'NAME OF EVENT', 'AUTHORITY OF EVENT', 'DATE OF EVENT',
         'DESCRIPTION OF EVENT', 'CERTIFICATE'])
    certificates = Certificate.objects.all().values_list('user', 'type_of_cert', 'name_of_event', 'auth_of_event',
                                                         'date_of_event', 'desc_of_event', 'upload_cert')
    for certificate in certificates:
        writer.writerow(certificate)

    return response


def generate_filter_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vstoreit_filter_students_report.csv" '
    if request.method == 'POST':
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        CB = request.POST.getlist('CB')
        writer = csv.writer(response)
        writer.writerow(['INFORMATION TECHNOLOGY'])
        writer.writerow([])
        if 'Information Technology' in CB:
            writer.writerow(['PROFILE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'FIRST NAME', 'LASTNAME', 'ROLL NO', 'EMAIL', 'ADDMISSION DATE', 'YEAR', 'BRANCH', 'DIV',
                 'MOBILE'])
            students = Student.objects.filter(branch='INFT').values_list('username', 'first_name', 'last_name',
                                                                         'roll_no', 'email', 'date_of_add',
                                                                         'year',
                                                                         'branch', 'div', 'mobile').filter(
                date_of_add__range=(fromdate, todate))

            for student in students:
                writer.writerow(student)

            writer.writerow([])
            writer.writerow(['EDUCATION DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'QUALIFICATION LEVEL', 'COUNTRY', 'STATE', 'DISTRICT', 'COLLEGE NAME', 'ADDMISSION YEAR',
                 'STREAM',
                 'COURSE NAME',
                 'RESULT', 'PASS YEAR', 'COMPLETED', 'PERCENTAGE', 'BOARD/UNIVERSITY NAME', 'MODE',
                 'ATTEMPTS TAKEN',
                 'MARKSHEET'])
            for student in students:
                educations = Education.objects.filter(user_id=student[0]).values_list('user', 'qua_level',
                                                                                      'country',
                                                                                      'state', 'district',
                                                                                      'college_name',
                                                                                      'admission_year',
                                                                                      'stream', 'course_name',
                                                                                      'result', 'pass_year',
                                                                                      'completed', 'percentage',
                                                                                      'board_university', 'mode',
                                                                                      'attempts',
                                                                                      'upload_marksheet')
                for education in educations:
                    writer.writerow(education)

            writer.writerow([])
            writer.writerow(['CERTIFICATE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'TYPE OF CERTIFICATE', 'NAME OF EVENT', 'AUTHORITY OF EVENT', 'DATE OF EVENT',
                 'DESCRIPTION OF EVENT', 'CERTIFICATE'])

            for student in students:
                certificates = Certificate.objects.filter(user_id=student[0]).values_list('user', 'type_of_cert',
                                                                                          'name_of_event',
                                                                                          'auth_of_event',
                                                                                          'date_of_event',
                                                                                          'desc_of_event',
                                                                                          'upload_cert')
                for certificate in certificates:
                    writer.writerow(certificate)

        writer.writerow(['COMPUTER ENGINEERING'])
        writer.writerow([])
        if 'Computer Engineering' in CB:
            writer.writerow(['PROFILE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'FIRST NAME', 'LASTNAME', 'ROLL NO', 'EMAIL', 'ADDMISSION DATE', 'YEAR', 'BRANCH', 'DIV',
                 'MOBILE'])
            students = Student.objects.filter(branch='CMPN').values_list('username', 'first_name', 'last_name',
                                                                         'roll_no', 'email', 'date_of_add',
                                                                         'year',
                                                                         'branch', 'div', 'mobile').filter(
                date_of_add__range=(fromdate, todate))
            for student in students:
                writer.writerow(student)
            writer.writerow([])
            writer.writerow(['EDUCATION DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'QUALIFICATION LEVEL', 'COUNTRY', 'STATE', 'DISTRICT', 'COLLEGE NAME', 'ADDMISSION YEAR',
                 'STREAM',
                 'COURSE NAME',
                 'RESULT', 'PASS YEAR', 'COMPLETED', 'PERCENTAGE', 'BOARD/UNIVERSITY NAME', 'MODE',
                 'ATTEMPTS TAKEN',
                 'MARKSHEET'])
            for student in students:
                educations = Education.objects.filter(user_id=student[0]).values_list('user', 'qua_level',
                                                                                      'country',
                                                                                      'state', 'district',
                                                                                      'college_name',
                                                                                      'admission_year',
                                                                                      'stream', 'course_name',
                                                                                      'result', 'pass_year',
                                                                                      'completed', 'percentage',
                                                                                      'board_university', 'mode',
                                                                                      'attempts',
                                                                                      'upload_marksheet')
                for education in educations:
                    writer.writerow(education)

            writer.writerow([])
            writer.writerow(['CERTIFICATE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'TYPE OF CERTIFICATE', 'NAME OF EVENT', 'AUTHORITY OF EVENT', 'DATE OF EVENT',
                 'DESCRIPTION OF EVENT', 'CERTIFICATE'])

            for student in students:
                certificates = Certificate.objects.filter(user_id=student[0]).values_list('user', 'type_of_cert',
                                                                                          'name_of_event',
                                                                                          'auth_of_event',
                                                                                          'date_of_event',
                                                                                          'desc_of_event',
                                                                                          'upload_cert')
                for certificate in certificates:
                    writer.writerow(certificate)

        writer.writerow(['ELECTRONICS AND TELECOMMUNICATION ENGINEERING'])
        writer.writerow([])
        if 'Electronics and Telecommunication Engineering' in CB:
            writer.writerow(['PROFILE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'FIRST NAME', 'LASTNAME', 'ROLL NO', 'EMAIL', 'ADDMISSION DATE', 'YEAR', 'BRANCH', 'DIV',
                 'MOBILE'])
            students = Student.objects.filter(branch='EXTC').values_list('username', 'first_name', 'last_name',
                                                                         'roll_no', 'email', 'date_of_add',
                                                                         'year',
                                                                         'branch', 'div', 'mobile').filter(
                date_of_add__range=(fromdate, todate))

            for student in students:
                writer.writerow(student)

            writer.writerow([])
            writer.writerow(['EDUCATION DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'QUALIFICATION LEVEL', 'COUNTRY', 'STATE', 'DISTRICT', 'COLLEGE NAME', 'ADDMISSION YEAR',
                 'STREAM',
                 'COURSE NAME',
                 'RESULT', 'PASS YEAR', 'COMPLETED', 'PERCENTAGE', 'BOARD/UNIVERSITY NAME', 'MODE',
                 'ATTEMPTS TAKEN',
                 'MARKSHEET'])
            for student in students:
                educations = Education.objects.filter(user_id=student[0]).values_list('user', 'qua_level',
                                                                                      'country',
                                                                                      'state', 'district',
                                                                                      'college_name',
                                                                                      'admission_year',
                                                                                      'stream', 'course_name',
                                                                                      'result', 'pass_year',
                                                                                      'completed', 'percentage',
                                                                                      'board_university', 'mode',
                                                                                      'attempts',
                                                                                      'upload_marksheet')
                for education in educations:
                    writer.writerow(education)

            writer.writerow([])
            writer.writerow(['CERTIFICATE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'TYPE OF CERTIFICATE', 'NAME OF EVENT', 'AUTHORITY OF EVENT', 'DATE OF EVENT',
                 'DESCRIPTION OF EVENT', 'CERTIFICATE'])

            for student in students:
                certificates = Certificate.objects.filter(user_id=student[0]).values_list('user', 'type_of_cert',
                                                                                          'name_of_event',
                                                                                          'auth_of_event',
                                                                                          'date_of_event',
                                                                                          'desc_of_event',
                                                                                          'upload_cert')
                for certificate in certificates:
                    writer.writerow(certificate)

        writer.writerow(['ELECTRONICS ENGINEERING'])
        writer.writerow([])
        if 'Electronics Engineering' in CB:
            writer.writerow(['PROFILE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'FIRST NAME', 'LASTNAME', 'ROLL NO', 'EMAIL', 'ADDMISSION DATE', 'YEAR', 'BRANCH', 'DIV',
                 'MOBILE'])
            students = Student.objects.filter(branch='ETRX').values_list('username', 'first_name', 'last_name',
                                                                         'roll_no', 'email', 'date_of_add',
                                                                         'year',
                                                                         'branch', 'div', 'mobile').filter(
                date_of_add__range=(fromdate, todate))

            for student in students:
                writer.writerow(student)

            writer.writerow([])
            writer.writerow(['EDUCATION DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'QUALIFICATION LEVEL', 'COUNTRY', 'STATE', 'DISTRICT', 'COLLEGE NAME', 'ADDMISSION YEAR',
                 'STREAM',
                 'COURSE NAME',
                 'RESULT', 'PASS YEAR', 'COMPLETED', 'PERCENTAGE', 'BOARD/UNIVERSITY NAME', 'MODE',
                 'ATTEMPTS TAKEN',
                 'MARKSHEET'])
            for student in students:
                educations = Education.objects.filter(user_id=student[0]).values_list('user', 'qua_level',
                                                                                      'country',
                                                                                      'state', 'district',
                                                                                      'college_name',
                                                                                      'admission_year',
                                                                                      'stream', 'course_name',
                                                                                      'result', 'pass_year',
                                                                                      'completed', 'percentage',
                                                                                      'board_university', 'mode',
                                                                                      'attempts',
                                                                                      'upload_marksheet')
                for education in educations:
                    writer.writerow(education)

            writer.writerow([])
            writer.writerow(['CERTIFICATE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'TYPE OF CERTIFICATE', 'NAME OF EVENT', 'AUTHORITY OF EVENT', 'DATE OF EVENT',
                 'DESCRIPTION OF EVENT', 'CERTIFICATE'])

            for student in students:
                certificates = Certificate.objects.filter(user_id=student[0]).values_list('user', 'type_of_cert',
                                                                                          'name_of_event',
                                                                                          'auth_of_event',
                                                                                          'date_of_event',
                                                                                          'desc_of_event',
                                                                                          'upload_cert')
                for certificate in certificates:
                    writer.writerow(certificate)

        writer.writerow(['BIOMEDICAL ENGINEEERING'])
        writer.writerow([])
        if 'Biomedical Engineering' in CB:
            writer.writerow(['PROFILE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'FIRST NAME', 'LASTNAME', 'ROLL NO', 'EMAIL', 'ADDMISSION DATE', 'YEAR', 'BRANCH', 'DIV',
                 'MOBILE'])
            students = Student.objects.filter(branch='BIOM').values_list('username', 'first_name', 'last_name',
                                                                         'roll_no', 'email', 'date_of_add',
                                                                         'year',
                                                                         'branch', 'div', 'mobile').filter(
                date_of_add__range=(fromdate, todate))

            for student in students:
                writer.writerow(student)

            writer.writerow([])
            writer.writerow(['EDUCATION DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'QUALIFICATION LEVEL', 'COUNTRY', 'STATE', 'DISTRICT', 'COLLEGE NAME', 'ADDMISSION YEAR',
                 'STREAM',
                 'COURSE NAME',
                 'RESULT', 'PASS YEAR', 'COMPLETED', 'PERCENTAGE', 'BOARD/UNIVERSITY NAME', 'MODE',
                 'ATTEMPTS TAKEN',
                 'MARKSHEET'])
            for student in students:
                educations = Education.objects.filter(user_id=student[0]).values_list('user', 'qua_level',
                                                                                      'country',
                                                                                      'state', 'district',
                                                                                      'college_name',
                                                                                      'admission_year',
                                                                                      'stream', 'course_name',
                                                                                      'result', 'pass_year',
                                                                                      'completed', 'percentage',
                                                                                      'board_university', 'mode',
                                                                                      'attempts',
                                                                                      'upload_marksheet')
                for education in educations:
                    writer.writerow(education)

            writer.writerow([])
            writer.writerow(['CERTIFICATE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'TYPE OF CERTIFICATE', 'NAME OF EVENT', 'AUTHORITY OF EVENT', 'DATE OF EVENT',
                 'DESCRIPTION OF EVENT', 'CERTIFICATE'])

            for student in students:
                certificates = Certificate.objects.filter(user_id=student[0]).values_list('user', 'type_of_cert',
                                                                                          'name_of_event',
                                                                                          'auth_of_event',
                                                                                          'date_of_event',
                                                                                          'desc_of_event',
                                                                                          'upload_cert')
                for certificate in certificates:
                    writer.writerow(certificate)

        writer.writerow(['MANAGEMENT STUDIES'])
        writer.writerow([])
        if 'Management Studies' in CB:
            writer.writerow(['PROFILE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'FIRST NAME', 'LASTNAME', 'ROLL NO', 'EMAIL', 'ADDMISSION DATE', 'YEAR', 'BRANCH', 'DIV',
                 'MOBILE'])
            students = Student.objects.filter(branch='manage').values_list('username', 'first_name', 'last_name',
                                                                           'roll_no', 'email', 'date_of_add',
                                                                           'year',
                                                                           'branch', 'div', 'mobile').filter(
                date_of_add__range=(fromdate, todate))

            for student in students:
                writer.writerow(student)

            writer.writerow([])
            writer.writerow(['EDUCATION DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'QUALIFICATION LEVEL', 'COUNTRY', 'STATE', 'DISTRICT', 'COLLEGE NAME', 'ADDMISSION YEAR',
                 'STREAM',
                 'COURSE NAME',
                 'RESULT', 'PASS YEAR', 'COMPLETED', 'PERCENTAGE', 'BOARD/UNIVERSITY NAME', 'MODE',
                 'ATTEMPTS TAKEN',
                 'MARKSHEET'])
            for student in students:
                educations = Education.objects.filter(user_id=student[0]).values_list('user', 'qua_level',
                                                                                      'country',
                                                                                      'state', 'district',
                                                                                      'college_name',
                                                                                      'admission_year',
                                                                                      'stream', 'course_name',
                                                                                      'result', 'pass_year',
                                                                                      'completed', 'percentage',
                                                                                      'board_university', 'mode',
                                                                                      'attempts',
                                                                                      'upload_marksheet')
                for education in educations:
                    writer.writerow(education)

            writer.writerow([])
            writer.writerow(['CERTIFICATE DETAILS'])
            writer.writerow([])
            writer.writerow(
                ['USERID', 'TYPE OF CERTIFICATE', 'NAME OF EVENT', 'AUTHORITY OF EVENT', 'DATE OF EVENT',
                 'DESCRIPTION OF EVENT', 'CERTIFICATE'])

            for student in students:
                certificates = Certificate.objects.filter(user_id=student[0]).values_list('user', 'type_of_cert',
                                                                                          'name_of_event',
                                                                                          'auth_of_event',
                                                                                          'date_of_event',
                                                                                          'desc_of_event',
                                                                                          'upload_cert')
                for certificate in certificates:
                    writer.writerow(certificate)

    return response


def contactus_done(request):
    return render(request, 'Contactus_done.html')
