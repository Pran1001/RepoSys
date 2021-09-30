from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Student, Certificate, Education


class StudentRegisterForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('username',)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2", "email"]


class StudentCertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'
        exclude = ('user',)


class StudentEducationForm(ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
        exclude = ('user',)


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)