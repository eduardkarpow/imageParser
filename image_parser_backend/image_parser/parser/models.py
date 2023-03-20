from django.db import models


# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=256)
    url = models.TextField()
    is_accepted = models.BooleanField(default=False)
