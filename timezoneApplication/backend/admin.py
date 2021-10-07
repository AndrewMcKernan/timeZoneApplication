from django.contrib import admin

# Register your models here.

from .models import Timezone

class TimezoneAdmin(admin.ModelAdmin):
    fields = ['name', 'city_name', 'difference_to_gmt', 'user']
    
admin.site.register(Timezone, TimezoneAdmin)