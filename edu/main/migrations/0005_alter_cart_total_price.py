# Generated by Django 4.2.5 on 2023-09-13 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]
