# Generated by Django 3.2.4 on 2021-09-28 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REPOSYSAPP', '0019_auto_20210926_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='date_of_add',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='div',
            field=models.DateField(),
        ),
    ]
