from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from .models import Student, Certificate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
