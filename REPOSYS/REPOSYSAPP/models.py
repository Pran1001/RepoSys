from django.db import models


# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=225)
    full_name = models.CharField(max_length=225, null=True)
    roll_no = models.CharField(max_length=225, null=True)
    email = models.EmailField(max_length=225, null=True)
    branch = models.CharField(max_length=225, null=True)
    mobile = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.full_name

