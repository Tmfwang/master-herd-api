# Generated by Django 3.1 on 2022-01-27 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Supervision',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_path', models.TextField()),
                ('when_started', models.CharField(max_length=150)),
                ('when_ended', models.CharField(max_length=150)),
                ('performed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('observation_longitude', models.FloatField()),
                ('observation_latitude', models.FloatField()),
                ('user_longitude', models.FloatField()),
                ('user_latitude', models.FloatField()),
                ('whenStarted', models.CharField(max_length=150)),
                ('type_observasjon', models.CharField(max_length=150)),
                ('sauFargeHvitOrGra', models.IntegerField(blank=True)),
                ('sauFargeBrun', models.IntegerField(blank=True)),
                ('sauFargeSort', models.IntegerField(blank=True)),
                ('soyeFargeHvitOrGra', models.IntegerField(blank=True)),
                ('soyeFargeBrun', models.IntegerField(blank=True)),
                ('soyeFargeSort', models.IntegerField(blank=True)),
                ('lamFargeHvitOrGra', models.IntegerField(blank=True)),
                ('lamFargeBrun', models.IntegerField(blank=True)),
                ('lamFargeSort', models.IntegerField(blank=True)),
                ('bjelleslipsFargeRod', models.IntegerField(blank=True)),
                ('bjelleslipsFargeBlaa', models.IntegerField(blank=True)),
                ('bjelleslipsFargeGulOrIngen', models.IntegerField(blank=True)),
                ('bjelleslipsFargeGronn', models.IntegerField(blank=True)),
                ('eiermerkeFarge', models.CharField(blank=True, max_length=150)),
                ('typeRovdyr', models.CharField(blank=True, max_length=150)),
                ('typeSkade', models.CharField(blank=True, max_length=150)),
                ('skadetSauFarge', models.CharField(blank=True, max_length=150)),
                ('skadetSauEiermerkeFarge', models.CharField(blank=True, max_length=150)),
                ('dodsarsak', models.CharField(blank=True, max_length=150)),
                ('dodSauFarge', models.CharField(blank=True, max_length=150)),
                ('dodSauEiermerkeFarge', models.CharField(blank=True, max_length=150)),
                ('supervision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supervision.supervision')),
            ],
        ),
    ]
