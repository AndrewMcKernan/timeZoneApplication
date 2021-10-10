from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('timezone', TimezoneViewSet, basename='timezone')

app_name = "backend"

urlpatterns = [
    path('', include(router.urls)),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('user-id', get_user_id, name="get-user-id"),
    path('users', get_users, name="get_users"),
    path('create-account', get_user_id, name="get-user-id"),
    path('make-superuser/<int:user_id>', get_user_id, name="get-user-id"),
    path('timezone-info/<str:city_name>', get_timezone_from_city, name="get-timezone-from-city"),
    path('timezone-info/<str:local_city_name>/<str:remote_city_name>', get_all_timezone_info_from_cities, name="get_all_timezone_info_from_cities")
]