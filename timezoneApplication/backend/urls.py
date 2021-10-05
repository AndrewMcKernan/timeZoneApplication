from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('timezone', TimezoneViewSet, basename='timezone')

urlpatterns = [
    path('', include(router.urls))
]