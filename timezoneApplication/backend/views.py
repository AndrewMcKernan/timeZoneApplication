from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from .models import Timezone
from .serializers import TimezoneSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.

class TimezoneViewSet(viewsets.ViewSet):

    permission_classes = [SessionAuthentication]

    def list(self, request):
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
        serializer = TimezoneSerializer(get_object_or_404(Timezone))
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