# Generated by Django 4.0.4 on 2022-06-06 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_options_customuser_unique_employee'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Employee'},
        ),
    ]
