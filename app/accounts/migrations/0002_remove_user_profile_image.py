# Generated by Django 2.2 on 2019-04-09 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_image',
        ),
    ]
