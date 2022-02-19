import json
from posixpath import split
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .models import User
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from django.contrib.auth.password_validation import validate_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login
from django.http import JsonResponse

class CreateUser(APIView):

    # def get(self, request, format=None):
    #   """
    #   Return a list of all users.
    #   """

    #   serializer = UserSerializer(User.objects.all(), many=True)
      
    #   return HttpResponse(serializer.data)
      # return Response(serializer.data)

    def post(self, request, format=json):
      if(request.data.get("password1") != request.data.get("password2") or not request.data.get("password1")):
        return HttpResponse('{"error": "Passordene stemmer ikke overens"}', status=status.HTTP_400_BAD_REQUEST)
      
      if(not request.data.get("full_name") or len(request.data.get("full_name").split(" ")) < 2):
        return HttpResponse('{"error": "Du mangler fullt navn"}', status=status.HTTP_400_BAD_REQUEST)
      
      if(not request.data.get("gaards_number") or len(request.data.get("gaards_number")) <= 3):
        return HttpResponse('{"error": "Du mangler gårdsnummer"}', status=status.HTTP_400_BAD_REQUEST)

      new_user = User(email=request.data.get("email").lower().strip(), full_name=request.data.get("full_name"), gaards_number=request.data.get("gaards_number"), bruks_number=request.data.get("bruks_number"), municipality=request.data.get("municipality"))
  
      try:
        validate_password(request.data.get("password1"), user=new_user)
        new_user.set_password(request.data.get("password1"))
      
      except Exception:
        return HttpResponse('{"error": "Passordet må være unikt nok, ikke bestå av kun tall, ikke bruke verdier som er tilknyttet brukeren din, og må ha en lengde på minst 8."}', status=status.HTTP_400_BAD_REQUEST)
  
      try:
        new_user.save()
      except Exception:
        return HttpResponse('{"error": "Noe gikk galt. Det er mulig at denne brukeren allerede eksisterer."}', status=status.HTTP_400_BAD_REQUEST)

      if(new_user):
        token = Token.objects.filter(user=new_user)[0]

        return HttpResponse(json.dumps({"token": str(token.key)}), status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_201_CREATED)
      
      else:
        return HttpResponse('{"error": "Noe gikk galt. Brukeren ble ikke opprettet."}', status=status.HTTP_400_BAD_REQUEST)
        #return Response(data='{"error": "Noe gikk galt. Brukeren ble ikke opprettet."}', status=status.HTTP_400_BAD_REQUEST)
     


# This is the view for logging in using session authentication, meant for use by the website. The mobile app uses token authentication.

class LoginHttpOnlyToken(APIView):
    def post(self, request, format=json):

      if(request.user.is_authenticated):
        return HttpResponse(json.dumps({"message": "Du er allerede logget inn"}), status=status.HTTP_200_OK)
      
      username = request.data.get('username')
      password = request.data.get('password')
      if username is None:
          return HttpResponse(json.dumps({"error": "Vennligst oppgi et brukernavn"}), status=status.HTTP_400_BAD_REQUEST)
      elif password is None:
          return HttpResponse(json.dumps({"error": "Vennligst oppgi et passord"}), status=status.HTTP_400_BAD_REQUEST)

      user = authenticate(username=username, password=password)
      if user is not None:
          token = Token.objects.filter(user=user)

          if(token.count() > 0):
            response = HttpResponse(json.dumps({"message": "Du har blitt logget inn"}), status=status.HTTP_200_OK)
            
            response.set_cookie(key='AuthorizationToken', value=str(token[0].key), httponly=True)

            return response
      return HttpResponse(json.dumps({"error": "Passordet eller brukernavnet er ugyldig"}), status=status.HTTP_400_BAD_REQUEST)


class VerifyLogin(APIView):
    def get(self, request, format=json):

      if(request.user.is_authenticated):
        return HttpResponse(json.dumps({"isLoggedIn": True}), status=status.HTTP_200_OK)

      else:
        token = Token.objects.filter(key=request.COOKIES.get("AuthorizationToken"))
        
        if(token.count() == 0):
          return HttpResponse(json.dumps({"isLoggedIn": False}), status=status.HTTP_200_OK)

        token_user = User.objects.filter(auth_token=token[0])
      
        if(not token_user.count() > 0):
          return HttpResponse(json.dumps({"isLoggedIn": False}), status=status.HTTP_200_OK)
        else:
          return HttpResponse(json.dumps({"isLoggedIn": True}), status=status.HTTP_200_OK)

