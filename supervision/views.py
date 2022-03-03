import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from django.http import HttpResponse
from django.db.models import Count

from .models import User
from rest_framework.authtoken.models import Token
from .models import Supervision, Observation

from datetime import datetime
from datetime import timedelta


def format_supervision(supervision):
  all_observations = []

  for o in Observation.objects.filter(supervision=supervision):
    observation_dict = {}

    observation_dict["observationLocation"] = {"latitude": o.observation_latitude, "longitude": o.observation_longitude}
    observation_dict["userLocation"] = {"latitude": o.user_latitude, "longitude": o.user_longitude}
    observation_dict["whenRegisteredDateTime"] = o.when_registered.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    observation_dict["observationDetails"] = {
      "alle": {
          "typeObservasjon": o.type_observasjon
      },
      
      "gruppeSau": {
        "fargePaSau": {
          "hvitOrGra": o.sauFargeHvitOrGra,
          "brun": o.sauFargeBrun,
          "sort": o.sauFargeSort
        },
        
        "fargePaSoye": {
          "hvitOrGra": o.soyeFargeHvitOrGra,
          "brun": o.soyeFargeBrun,
          "sort": o.soyeFargeSort
        },
        
        "fargePaLam": {
          "hvitOrGra": o.lamFargeHvitOrGra,
          "brun": o.lamFargeBrun,
          "sort": o.lamFargeSort
        },
        
        "fargePaBjelleslips": {
          "rod": o.bjelleslipsFargeRod,
          "bla": o.bjelleslipsFargeBlaa,
          "gulOrIngen": o.bjelleslipsFargeGulOrIngen,
          "gronn": o.bjelleslipsFargeGronn
        },
        
        "fargePaEiermerke": json.loads(o.eiermerkeFarge)

      },
      "rovdyr": {
          "typeRovdyr": o.typeRovdyr
      },
      "skadetSau": {
          "typeSkade": o.skadetSauTypeSkade,
          "fargePaSau": o.skadetSauFarge,
          "fargePaEiermerke": o.skadetSauEiermerkeFarge
      },
      "dodSau": {
          "dodsarsak": o.dodSauDodsarsak,
          "fargePaSau": o.dodSauFarge,
          "fargePaEiermerke": o.dodSauEiermerkeFarge
      }
    }

    all_observations.append(observation_dict)

  supervision_dict = {}
  supervision_dict["id"] = str(supervision.id)
  supervision_dict["allObservations"] = all_observations
  supervision_dict["fullPath"] = json.loads(supervision.full_path)
  supervision_dict["whenStarted"] = supervision.when_started.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
  supervision_dict["whenEnded"] = supervision.when_ended.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

  return supervision_dict


class GetSupervision(APIView):
  # Fetches a single supervision with accompanying observations. The supervision must belong to the user that performs the request.
  def get(self, request, id, format=None):
    if(not request.user.is_authenticated):
      return HttpResponse(status=status.HTTP_403_FORBIDDEN)
    try:
      supervision = Supervision.objects.filter(id=id)

    except Exception as e:
      return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if(supervision.count() == 0):
      return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if(supervision[0].performed_by != request.user):
      return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
      
    return HttpResponse(json.dumps(format_supervision(supervision[0])), status=status.HTTP_200_OK)

  def delete(self, request, id, format=None):
    
    # The authentication token is usually a part of the cookies (as a HttpOnly cookie). 
    # This sets the request.user to the correct user if that is the case.
    if(not request.user.is_authenticated):
      token = Token.objects.filter(key=request.COOKIES.get("AuthorizationToken"))
      
      if(token.count() == 0):
        return HttpResponse(json.dumps({"error": "Ikke logget inn"}), status=status.HTTP_401_UNAUTHORIZED)

      token_user = User.objects.filter(auth_token=token[0])
    
      if(not token_user.count() > 0):
        return HttpResponse(json.dumps({"error": "Ikke logget inn"}), status=status.HTTP_401_UNAUTHORIZED)
      else:
        request.user = token_user[0]

    try:
      supervision = Supervision.objects.filter(id=id)

    except Exception as e:
      return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if(supervision.count() == 0):
      return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if(supervision[0].performed_by != request.user):
      return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
      
    supervision.delete()  
    return HttpResponse(status=status.HTTP_200_OK)


class GetSupervisions(APIView):

  # Fetches all supervisions (with accompanying observations) that belongs to the user that performs the request.
  def get(self, request, format=None):

    # The authentication token is usually a part of the cookies (as a HttpOnly cookie). 
    # This sets the request.user to the correct user if that is the case.
    if(not request.user.is_authenticated):
      token = Token.objects.filter(key=request.COOKIES.get("AuthorizationToken"))
      
      if(token.count() == 0):
        return HttpResponse(json.dumps({"error": "Ikke logget inn"}), status=status.HTTP_401_UNAUTHORIZED)

      token_user = User.objects.filter(auth_token=token[0])
    
      if(not token_user.count() > 0):
        return HttpResponse(json.dumps({"error": "Ikke logget inn"}), status=status.HTTP_401_UNAUTHORIZED)
      else:
        request.user = token_user[0]


    users_supervisions = Supervision.objects.filter(performed_by=request.user)

    # Filtering
    if(request.GET.get("filterDateStart")):
      users_supervisions = users_supervisions.filter(when_started__gte=datetime.strptime(request.GET.get("filterDateStart"), "%Y-%m-%d"))

    if(request.GET.get("filterDateEnd")):
      users_supervisions = users_supervisions.filter(when_started__lte=(datetime.strptime(request.GET.get("filterDateEnd"), "%Y-%m-%d") + timedelta(days=1)))

    # Sorting
    if(request.GET.get("sortBy") == "tilsynsdato"):
      users_supervisions = users_supervisions.order_by("when_started")
          
    elif(request.GET.get("sortBy") == "observasjoner"):
      users_supervisions = users_supervisions.annotate(num_observations=Count('observation')).order_by('num_observations')
      
    elif(request.GET.get("sortBy") == "varighet"):
      users_supervisions = users_supervisions.extra(select={'offset': 'when_ended - when_started'}).order_by('offset')
      
    if(request.GET.get("isDescendingSort") == "true"):
        users_supervisions = users_supervisions.reverse()  
      

    supervisions_response = []

    for supervision in users_supervisions:
      supervisions_response.append(format_supervision(supervision))
      
    return HttpResponse(json.dumps(supervisions_response), status=status.HTTP_200_OK, content_type='application/json')

  # Creates a supervision database object (with accompanying observations), that is set to belong to the user that performs the request.
  def post (self, request, format=json):
   
    # The authentication token is usually a part of the cookies (as a HttpOnly cookie). 
    # This sets the request.user to the correct user if that is the case.
    if(not request.user.is_authenticated):
      token = Token.objects.filter(key=request.COOKIES.get("AuthorizationToken"))
      
      if(token.count() == 0):
        return HttpResponse(json.dumps({"error": "Ikke logget inn"}), status=status.HTTP_401_UNAUTHORIZED)

      token_user = User.objects.filter(auth_token=token[0])
    
      if(not token_user.count() > 0):
        return HttpResponse(json.dumps({"error": "Ikke logget inn"}), status=status.HTTP_401_UNAUTHORIZED)
      else:
        request.user = token_user[0]

    existing_supervision = Supervision.objects.filter(when_started=request.data.get("whenStarted")).count()

    if(existing_supervision > 0):
      return Response(status=status.HTTP_200_OK)

    new_supervision = Supervision(full_path=json.dumps(request.data.get("fullPath")), when_started=datetime.strptime(request.data.get("whenStarted"), "%Y-%m-%dT%H:%M:%S.%fZ"), when_ended=datetime.strptime(request.data.get("whenEnded"), "%Y-%m-%dT%H:%M:%S.%fZ"), performed_by=request.user)

    new_observations = []

    for observation in request.data.get("allObservations"):
      new_observations.append(
        Observation(
          supervision=new_supervision, 
          observation_longitude=observation.get("observationLocation").get("longitude"),
          observation_latitude=observation.get("observationLocation").get("latitude"),
          user_longitude=observation.get("userLocation").get("longitude"),
          user_latitude=observation.get("userLocation").get("latitude"),
          when_registered=datetime.strptime(observation.get("whenRegisteredDateTime"), "%Y-%m-%dT%H:%M:%S.%fZ"),
          type_observasjon=observation.get("observationDetails").get("alle").get("typeObservasjon"), 
          
          # Gruppe sau
          sauFargeHvitOrGra=observation.get("observationDetails").get("gruppeSau").get("fargePaSau").get("hvitOrGra"),
          sauFargeBrun=observation.get("observationDetails").get("gruppeSau").get("fargePaSau").get("brun"),
          sauFargeSort=observation.get("observationDetails").get("gruppeSau").get("fargePaSau").get("sort"),
          soyeFargeHvitOrGra=observation.get("observationDetails").get("gruppeSau").get("fargePaSoye").get("hvitOrGra"),
          soyeFargeBrun=observation.get("observationDetails").get("gruppeSau").get("fargePaSoye").get("brun"),
          soyeFargeSort=observation.get("observationDetails").get("gruppeSau").get("fargePaSoye").get("sort"),
          lamFargeHvitOrGra=observation.get("observationDetails").get("gruppeSau").get("fargePaLam").get("hvitOrGra"),
          lamFargeBrun=observation.get("observationDetails").get("gruppeSau").get("fargePaLam").get("brun"),
          lamFargeSort=observation.get("observationDetails").get("gruppeSau").get("fargePaLam").get("sort"),
          bjelleslipsFargeRod=observation.get("observationDetails").get("gruppeSau").get("fargePaBjelleslips").get("rod"),
          bjelleslipsFargeBlaa=observation.get("observationDetails").get("gruppeSau").get("fargePaBjelleslips").get("bla"),
          bjelleslipsFargeGulOrIngen=observation.get("observationDetails").get("gruppeSau").get("fargePaBjelleslips").get("gulOrIngen"),
          bjelleslipsFargeGronn=observation.get("observationDetails").get("gruppeSau").get("fargePaBjelleslips").get("gronn"),
          eiermerkeFarge=json.dumps(observation.get("observationDetails").get("gruppeSau").get("fargePaEiermerke")),
          
          # Type rovdyr
          typeRovdyr=observation.get("observationDetails").get("rovdyr").get("typeRovdyr"),

          # Skadet sau
          skadetSauTypeSkade=observation.get("observationDetails").get("skadetSau").get("typeSkade"),
          skadetSauFarge=observation.get("observationDetails").get("skadetSau").get("fargePaSau"),
          skadetSauEiermerkeFarge=observation.get("observationDetails").get("skadetSau").get("fargePaEiermerke"),
          
          # Dod sau
          dodSauDodsarsak=observation.get("observationDetails").get("dodSau").get("dodsarsak"),
          dodSauFarge=observation.get("observationDetails").get("dodSau").get("fargePaSau"),
          dodSauEiermerkeFarge=observation.get("observationDetails").get("dodSau").get("fargePaEiermerke"),   
        )
      )
      
    new_supervision.save()

    for observation in new_observations:
      observation.save()

    return HttpResponse(status=status.HTTP_201_CREATED)
