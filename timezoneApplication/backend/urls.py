from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('timezone', TimezoneViewSet, basename='timezone')

app_name = "backend"

urlpatterns = [
    path('', include(router.urls)),
    path('login', login_view, name="login"),
    path('user_id', get_user_id, name="get-user-id"),
    path('timezone_info/<str:city_name>', get_timezone_from_city, name="get-timezone-from-city")
]