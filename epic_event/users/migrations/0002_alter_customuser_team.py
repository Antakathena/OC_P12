# Generated by Django 4.0.4 on 2022-05-25 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='team',
            field=models.CharField(choices=[('management', 'management'), ('sales', 'sales'), ('support', 'support')], default='management', max_length=10),
        ),
    ]
