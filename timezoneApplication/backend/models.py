from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class Timezone(models.Model):
    name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    difference_to_gmt = models.IntegerField(validators=[MinValueValidator(-12), MaxValueValidator(14)])
    user = models.ForeignKey('User', on_delete=models.CASCADE)