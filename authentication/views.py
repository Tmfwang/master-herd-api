import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .models import User
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from django.contrib.auth.password_validation import validate_password

class ListUsers(APIView):

    # def get(self, request, format=None):
    #   """
    #   Return a list of all users.
    #   """

    #   serializer = UserSerializer(User.objects.all(), many=True)
      
    #   return HttpResponse(serializer.data)
      # return Response(serializer.data)


    def post (self, request, format=json):
      
      if(request.data.get("password1") != request.data.get("password2") or not request.data.get("password1")):
        return HttpResponse('{"error": "Passordene stemmer ikke overens"}', status=status.HTTP_400_BAD_REQUEST)
        # return Response(data='{"error": "Passordene stemmer ikke overens"}', status=status.HTTP_400_BAD_REQUEST)


      try:
        validate_password(request.data.get("password1"))
      
      except Exception as e:
        return HttpResponse('{"error": "Passordet må være unikt nok, ikke bestå av kun tall, ikke bruke verdier som er tilknyttet brukeren din, og må ha en lengde på minst 8."}', status=status.HTTP_400_BAD_REQUEST)
        

      if(User.objects.filter(email=request.data.get("email").lower()).count() > 0):
        return HttpResponse('{"error": "Denne e-post-adressen har allerede blitt brukt"}', status=status.HTTP_400_BAD_REQUEST)
        
      new_user = User.objects.create(email=request.data.get("email").lower(), password=request.data.get("password1"), full_name=request.data.get("full_name"), gaards_number=request.data.get("gaards_number"), bruks_number=request.data.get("bruks_number"), municipality=request.data.get("municipality"))

      if(new_user):
        token = Token.objects.filter(user=new_user)[0]

        return HttpResponse(json.dumps({"token": str(token.key)}), status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_201_CREATED)
      
      else:
        return HttpResponse('{"error": "Noe gikk galt. Brukeren ble ikke opprettet."}', status=status.HTTP_400_BAD_REQUEST)
        #return Response(data='{"error": "Noe gikk galt. Brukeren ble ikke opprettet."}', status=status.HTTP_400_BAD_REQUEST)
     