# Generated by Django 3.1b1 on 2020-06-26 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campionat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etapa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numar_etapa', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Meci',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gazda', models.CharField(max_length=50)),
                ('oaspete', models.CharField(max_length=50)),
                ('scor', models.CharField(max_length=250)),
                ('etapa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campionat.etapa')),
            ],
        ),
        migrations.AddField(
            model_name='echipa',
            name='etapa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='campionat.etapa'),
            preserve_default=False,
        ),
    ]
