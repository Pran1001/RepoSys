from django.contrib.auth.models import User
from django.db import models

# Create your models here.

YEARS = (
    (u'FE', u'FE'),
    (u'SE', u'SE'),
    (u'TE', u'TE'),
    (u'BE', u'BE'),
)

DIV = (
    (u'A', u'A'),
    (u'B', u'B'),
)

BRANCH = (
    (u'INFT', u'Information Technology'),
    (u'CMPN', u'Computer Engineering'),
    (u'ETRX', u'Electronics Engieering'),
    (u'EXTC', u'Electronics and Telecommunication Engineering'),
    (u'BIOM', u'Biomedical Engineering'),
    (u'MNGT', u'Management Studies'),
)


class Student(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=225, null=True)
    last_name = models.CharField(max_length=225, null=True)
    roll_no = models.CharField(max_length=225, null=True)
    email = models.EmailField(max_length=225, null=True)
    branch = models.CharField(max_length=45, choices=BRANCH, default="")
    year = models.CharField(max_length=30, choices=YEARS, default="")
    div = models.CharField(max_length=30, choices=DIV, default="")
    mobile = models.CharField(max_length=10, null=True)
    profile_image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type_of_cert = models.CharField(max_length=225, null=True)
    name_of_event = models.CharField(max_length=225, null=True)
    auth_of_event = models.CharField(max_length=225, null=True)
    date_of_event = models.DateField()
    desc_of_event = models.CharField(max_length=225, null=True)
    upload_cert = models.FileField(upload_to="certificates/%Y/%m/%d/", null=True, blank=True)
