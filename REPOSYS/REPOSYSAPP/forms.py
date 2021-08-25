from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

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

