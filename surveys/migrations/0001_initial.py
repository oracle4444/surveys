# Generated by Django 3.2 on 2021-05-06 14:09

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Surveys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2021, 5, 6, 14, 9, 14, 97294, tzinfo=utc), editable=False, verbose_name='start date')),
                ('finish_date', models.DateTimeField(verbose_name='finish date')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('text', 'question with a text answer'), ('single', 'question with a single choice answer'), ('multiple', 'question with a multiple choice answer')], max_length=50)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.surveys')),
            ],
        ),
    ]