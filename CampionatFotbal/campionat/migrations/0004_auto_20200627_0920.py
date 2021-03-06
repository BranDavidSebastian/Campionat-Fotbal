# Generated by Django 3.1b1 on 2020-06-27 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campionat', '0003_auto_20200626_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clasament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etapa', models.IntegerField()),
                ('echipa', models.CharField(max_length=250)),
                ('victorii', models.IntegerField()),
                ('egaluri', models.IntegerField()),
                ('infrangeri', models.IntegerField()),
                ('goluri_primite', models.IntegerField()),
                ('goluri_inscrise', models.IntegerField()),
                ('ultimele_rezultate', models.CharField(max_length=50)),
                ('loc_anterior', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='echipa',
            name='egaluri',
        ),
        migrations.RemoveField(
            model_name='echipa',
            name='etapa',
        ),
        migrations.RemoveField(
            model_name='echipa',
            name='goluri_inscrise',
        ),
        migrations.RemoveField(
            model_name='echipa',
            name='goluri_primite',
        ),
        migrations.RemoveField(
            model_name='echipa',
            name='infrangeri',
        ),
        migrations.RemoveField(
            model_name='echipa',
            name='victorii',
        ),
        migrations.AddField(
            model_name='meci',
            name='tip',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meci',
            name='etapa',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Etapa',
        ),
    ]
