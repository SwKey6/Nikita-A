# Generated by Django 5.2.3 on 2025-06-24 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_appointment_user_alter_clientappointment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='do',
            field=models.CharField(max_length=100, null=True, verbose_name='Что умеет'),
        ),
        migrations.AddField(
            model_name='employee',
            name='prof',
            field=models.CharField(max_length=100, null=True, verbose_name='Направление'),
        ),
        migrations.AddField(
            model_name='employee',
            name='worked',
            field=models.CharField(max_length=100, null=True, verbose_name='Опыт работы(в годах)'),
        ),
    ]
