from django.db import models
import uuid
from authentication.models import User


class Supervision(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  performed_by = models.ForeignKey(User, on_delete=models.CASCADE)

  full_path = models.TextField()
  when_started = models.CharField(max_length=150)
  when_ended = models.CharField(max_length=150)
  

class Observation(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  supervision = models.ForeignKey(Supervision, on_delete=models.CASCADE)

  observation_longitude = models.FloatField()
  observation_latitude = models.FloatField()
  user_longitude = models.FloatField()
  user_latitude = models.FloatField()
  when_registered = models.CharField(max_length=150)
  
  type_observasjon =  models.CharField(max_length=150)

  # Gruppe sau
  sauFargeHvitOrGra = models.IntegerField(blank=True)
  sauFargeBrun = models.IntegerField(blank=True)
  sauFargeSort = models.IntegerField(blank=True)
  
  soyeFargeHvitOrGra = models.IntegerField(blank=True)
  soyeFargeBrun = models.IntegerField(blank=True)
  soyeFargeSort = models.IntegerField(blank=True)

  lamFargeHvitOrGra = models.IntegerField(blank=True)
  lamFargeBrun = models.IntegerField(blank=True)
  lamFargeSort = models.IntegerField(blank=True)

  bjelleslipsFargeRod = models.IntegerField(blank=True)
  bjelleslipsFargeBlaa = models.IntegerField(blank=True)
  bjelleslipsFargeGulOrIngen = models.IntegerField(blank=True)
  bjelleslipsFargeGronn = models.IntegerField(blank=True)

  eiermerkeFarge = models.TextField(blank=True)

  # Rovdyr
  typeRovdyr = models.CharField(max_length=150, blank=True)

  # Skadet sau
  skadetSauTypeSkade = models.CharField(max_length=150, blank=True)
  skadetSauFarge = models.CharField(max_length=150, blank=True)
  skadetSauEiermerkeFarge = models.CharField(max_length=150, blank=True)

  # Død sau
  dodSauDodsarsak = models.CharField(max_length=150, blank=True)
  dodSauFarge = models.CharField(max_length=150, blank=True)
  dodSauEiermerkeFarge = models.CharField(max_length=150, blank=True)


  


  



