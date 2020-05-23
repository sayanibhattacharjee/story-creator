from django.db import models


# Create your models here.
class Grapher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Asset(models.Model):
    asset_name = models.CharField(max_length=50)
    is_asset_image = models.BooleanField(default=True)
    asset_file = models.FileField(upload_to="")


class Story(models.Model):
    grapher_id = models.IntegerField()
    story_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    duration = models.DurationField(null=True, blank=True)
    asset_id = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
