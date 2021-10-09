from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class Timezone(models.Model):
    name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # see https://stackoverflow.com/questions/34305805/foreignkey-user-in-models
    class Meta:
        permissions = (
            ("is_admin_user", "Admin User"),
        )