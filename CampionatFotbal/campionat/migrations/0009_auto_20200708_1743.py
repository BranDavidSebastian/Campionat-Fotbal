# Generated by Django 3.1b1 on 2020-07-08 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campionat', '0008_meci_tip_meci'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meci',
            name='jucat',
        ),
        migrations.RemoveField(
            model_name='meci',
            name='tip_meci',
        ),
    ]
