from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from cdp_db_site import settings


# Disc group as defined in the player.
class Group(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True, validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200)
    color = ColorField(format="hex")


# Disc in the player
class Disc(models.Model):
    position = models.PositiveSmallIntegerField(primary_key=True,
                                                validators=[MinValueValidator(1), MaxValueValidator(settings.CDP_SIZE)])
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)