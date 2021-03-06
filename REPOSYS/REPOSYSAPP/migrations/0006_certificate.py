# Generated by Django 3.2.6 on 2021-08-16 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REPOSYSAPP', '0005_auto_20210816_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_cert', models.CharField(max_length=225, null=True)),
                ('name_of_event', models.CharField(max_length=225, null=True)),
                ('auth_of_event', models.CharField(max_length=225, null=True)),
                ('date_of_event', models.DateField()),
                ('desc_of_event', models.CharField(max_length=225, null=True)),
                ('upload_cert', models.FileField(blank=True, null=True, upload_to='certificates/%Y/%m/%d/')),
            ],
        ),
    ]
