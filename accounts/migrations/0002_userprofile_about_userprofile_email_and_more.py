# Generated by Django 5.0.2 on 2024-05-03 14:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='about',
            field=models.CharField(blank=True, max_length=1000, verbose_name='About...'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=30, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='headline',
            field=models.CharField(blank=True, max_length=20, verbose_name='Headline'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mainSkills',
            field=models.CharField(blank=True, max_length=50, verbose_name='Main Skills'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Full name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(blank=True, max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
