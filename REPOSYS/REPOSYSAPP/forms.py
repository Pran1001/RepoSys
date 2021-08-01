from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from .models import Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['username', 'email', 'password1', 'password2']

