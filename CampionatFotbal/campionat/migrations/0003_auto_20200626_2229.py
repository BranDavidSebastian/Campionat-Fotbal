# Generated by Django 3.1b1 on 2020-06-26 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campionat', '0002_auto_20200626_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='echipa',
            name='etapa',
            field=models.IntegerField(),
        ),
    ]
