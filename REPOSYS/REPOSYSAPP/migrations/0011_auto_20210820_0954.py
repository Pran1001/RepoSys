# Generated by Django 3.2.6 on 2021-08-20 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REPOSYSAPP', '0010_remove_certificate_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='div',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B')], default='', max_length=30),
        ),
        migrations.AddField(
            model_name='student',
            name='year',
            field=models.CharField(choices=[('FE', 'FE'), ('SE', 'SE'), ('TE', 'TE'), ('BE', 'BE')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(choices=[('INFT', 'Information Technology'), ('CMPN', 'Computer Engineering'), ('ETRX', 'Electronics Engieering'), ('EXTC', 'Electronics and Telecommunication Engineering'), ('BIOM', 'Biomedical Engineering'), ('MNGT', 'Management Studies')], default='', max_length=45),
        ),
    ]
