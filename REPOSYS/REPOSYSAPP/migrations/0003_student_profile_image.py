# Generated by Django 3.2.6 on 2021-08-15 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REPOSYSAPP', '0002_alter_student_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]