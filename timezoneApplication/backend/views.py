from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication

# Create your views here.

class TimezoneViewSet(viewsets.ViewSet):

    permission_classes = [SessionAuthentication]

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass