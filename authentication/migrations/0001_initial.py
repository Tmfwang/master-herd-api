# Generated by Django 3.1.8 on 2022-03-01 17:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=300, unique=True)),
                ('email', models.EmailField(max_length=150, verbose_name='email address')),
                ('full_name', models.CharField(max_length=150)),
                ('gaards_number', models.CharField(max_length=150)),
                ('bruks_number', models.CharField(blank=True, max_length=150, null=True)),
                ('municipality', models.CharField(blank=True, max_length=150, null=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('email', 'gaards_number')},
            },
        ),
    ]
