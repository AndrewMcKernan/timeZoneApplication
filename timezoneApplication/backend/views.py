from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from .models import Timezone
from .serializers import TimezoneSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
#import requests
#from geopy import geocoders
from pytz import timezone
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import datetime
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Create your views here.

class TimezoneViewSet(viewsets.ViewSet):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        # list either only the timezones we own, or all of them, depending on permissions
        if request.user.is_superuser:
            timezones = Timezone.objects.all()
        else:
            timezones = Timezone.objects.filter(user=request.user.id)
        serializer = TimezoneSerializer(timezones, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TimezoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_string = ""
            for error in serializer.errors:
                error_string += error + " "
            return Response(error_string, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        timezone = get_object_or_404(Timezone, pk=pk)
        serializer = TimezoneSerializer(timezone)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        # do not allow modification of a timezone belonging to someone else if we are not a superuser
        current_timezone_obj = get_object_or_404(Timezone, pk=pk)
        if current_timezone_obj.user != request.user.id and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # do not allow author to be changed if we are not a superuser
        if str(request.POST['user']) != str(request.user.id) and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = TimezoneSerializer(current_timezone_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_200_OK)
        else:
            error_string = ""
            for error in serializer.errors:
                error_string += error + " "
            return Response(error_string, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        timezone = get_object_or_404(Timezone, pk=pk)
        timezone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_timezone_from_city(request, city_name):
    # first, get geo location from city name
    geolocator = Nominatim(user_agent="timezoneToptalApplication")
    location = geolocator.geocode(city_name)
    if location is None:
        # there is no location matching the inputted string
        return Response("No location matches the inputted name.", status=status.HTTP_400_BAD_REQUEST)
    obj = TimezoneFinder()
    city_timezone = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    city_timezone_now = datetime.datetime.now(timezone(city_timezone))
    gmt_offset = city_timezone_now.utcoffset().total_seconds()/60/60
    data = {'gmt_offset':gmt_offset}
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_all_timezone_info_from_cities(request, local_city_name, remote_city_name):
    # first, get geo location from city name
    geolocator = Nominatim(user_agent="timezoneToptalApplication")
    remote_location = geolocator.geocode(remote_city_name)
    obj = TimezoneFinder()
    remote_city_timezone = obj.timezone_at(lng=remote_location.longitude, lat=remote_location.latitude)
    remote_city_timezone_now = datetime.datetime.now(timezone(remote_city_timezone))
    remote_gmt_offset = remote_city_timezone_now.utcoffset().total_seconds()/60/60
    
    local_location = geolocator.geocode(local_city_name)
    local_city_timezone = obj.timezone_at(lng=local_location.longitude, lat=local_location.latitude)
    local_city_timezone_now = datetime.datetime.now(timezone(local_city_timezone))
    local_gmt_offset = local_city_timezone_now.utcoffset().total_seconds()/60/60
    
    data = {'remote_gmt_offset':remote_gmt_offset, 'local_gmt_offset':local_gmt_offset, 'remote_city_timezone_now':remote_city_timezone_now, 'local_city_timezone_now':local_city_timezone_now, 'offset_diff':remote_gmt_offset - local_gmt_offset}
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request._request, user)
            if user.is_superuser:
                data = {'is_superuser':'True'}
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                data = {'is_superuser':'False'}
                return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])  
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticatedOrReadOnly])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
            
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_user_id(request):
    data = {'id':request.user.id}
    return Response(data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def create_account(request):
    new_user = User()
    new_user.username = request.POST['username']
    if request.POST['password'] != request.POST['confirm-password']:
        # they need to be the same
        return Response("The passwords do not match.", status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_password(request.POST['password'])
    except ValidationError as e:
        response_str = ""
        for error in e.messages:
            response_str += error + " "
        return Response(response_str, status=status.HTTP_400_BAD_REQUEST)
    new_user.set_password(request.POST['password'])
    try:
        new_user.save()
    except IntegrityError:
        return Response("A user with this username already exists", status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])  
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticatedOrReadOnly])
def make_superuser(request, user_id):
    if request.user.id == user_id:
        # do not allow them to modify themselves
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
        user.is_superuser = False
        user.is_staff = False
        user.is_admin = False
        user.is_superuser = False
        user.save()
    else:
        user.is_superuser = True
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
    return Response(status=status.HTTP_200_OK)
    
@api_view(['GET'])  
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_users(request):
    # only available to superusers
    if not request.user.is_superuser:
        return Response(status=status.HTTP_403_FORBIDDEN)
    # do not include the user that we are, since we should not modify our own permissions
    users = User.objects.exclude(pk=request.user.id)
    data = []
    for user in users:
        data.append({'username':user.username, 'is_superuser':user.is_superuser, 'id':user.id})
    return Response(data=data, status=status.HTTP_200_OK)
    
@api_view(['GET'])  
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_authors(request):
    # only available to superusers
    if not request.user.is_superuser:
        return Response(status=status.HTTP_403_FORBIDDEN)
    # include the user that we are - this is for the purpose of selecting an author.
    users = User.objects.all()
    data = []
    for user in users:
        data.append({'username':user.username, 'is_superuser':user.is_superuser, 'id':user.id})
    return Response(data=data, status=status.HTTP_200_OK)