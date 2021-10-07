from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from .models import Timezone
from .serializers import TimezoneSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class TimezoneViewSet(viewsets.ViewSet):

    authentication_classes = [SessionAuthentication]

    def list(self, request):
        # TODO: list either only the timezones we own, or all of them, depending on permissions
        timezones = Timezone.objects.all()
        serializer = TimezoneSerializer(timezones, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TimezoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        timezone = get_object_or_404(Timezone, pk=pk)
        serializer = TimezoneSerializer(timezone)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        # do not allow author to be changed if the permissions are not correct
        current_timezone_obj = get_object_or_404(Timezone, pk=pk)
        #if request.data['user'] != current_timezone_obj.user:
        #    return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = TimezoneSerializer(current_timezone_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        timezone = get_object_or_404(Timezone, pk=pk)
        timezone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request._request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
def get_user_id(request):
    data = {'id':request.user.id}
    return Response(data, status=status.HTTP_200_OK)
# TODO: create account creation, logout, and permission modifification functions