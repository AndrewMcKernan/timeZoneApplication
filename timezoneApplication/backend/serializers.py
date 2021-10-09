from rest_framework import serializers

from .models import Timezone

class TimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timezone
        fields = ['id', 'name', 'city_name', 'user']
        #fields = '__all__'