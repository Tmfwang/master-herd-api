from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Supervision, Observation
from .models import User

class ObservationSerializer(ModelSerializer):

  class Meta:
      model = Observation
      fields = (
          '__all__'
      )

class SupervisionSerializer(ModelSerializer):
  allObservations = ObservationSerializer(many=True)


  class Meta:
      model = Supervision
      fields = (
          '__all__'
      )