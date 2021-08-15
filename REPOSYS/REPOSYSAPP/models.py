from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Student(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=225, null=True)
    roll_no = models.CharField(max_length=225, null=True)
    email = models.EmailField(max_length=225, null=True)
    branch = models.CharField(max_length=225, null=True)
    mobile = models.CharField(max_length=10, null=True)
    profile_image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return self.full_name



