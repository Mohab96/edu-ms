# Generated by Django 4.2.5 on 2023-09-12 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_user_is_instructor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_instructor',
        ),
    ]
