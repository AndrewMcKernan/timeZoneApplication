from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('timezone', TimezoneViewSet, basename='timezone')

app_name = "backend"

urlpatterns = [
    path('', include(router.urls)),
    path('login', login_view, name="login"),
    path('user_id', get_user_id, name="get-user-id")
]