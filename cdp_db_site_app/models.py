import os

import django.core.exceptions
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from cdp_db_site import settings


# Disc group as defined in the player.
class Group(models.Model):
    title = models.CharField(max_length=200)
    color = ColorField(format="hex")
    def __str__(self):
        return self.title

    def as_json(self):
        return {"id": self.id, "title": self.title, "color": self.color}


# Disc in the player
class Disc(models.Model):
    position = models.PositiveSmallIntegerField(primary_key=True,
                                                validators=[MinValueValidator(1), MaxValueValidator(settings.CDP_SIZE)])
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, upload_to="images/")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"Disc #{self.position}/{settings.CDP_SIZE}: {self.title}"

    def as_json(self):
        try:
            return {"position": self.position, "title": self.title, "image": self.image.url,
                  "group": self.group_id}
        except ValueError:
            return {"position": self.position, "title": self.title, "image": None,
                    "group": self.group_id}
        
    # When image is changed, check if it is being used anywhere else. If not, remove it!
    def save(self, *args, **kwargs):
        self._check_image_change()
        super().save(*args, **kwargs)
    # When disc is deleted, check if image is being used anywhere else. If not, delete it!
    def delete(self, *args, **kwargs):
        self._check_image_change()
        super().delete(*args, **kwargs)

    def _check_image_change(self):
        try:
            # Don't run if the SAVED version of me has no image
            saved_self = Disc.objects.get(position = self.position)
            if not saved_self.image:
                print("I don't yet have an image!")
                return
        except django.core.exceptions.ObjectDoesNotExist:
            # I don't exist yet! No need to check for stray past images.
            print("I don't exist!")
            return

        # Image was changed. Remove the old one!
        os.remove(settings.MEDIA_ROOT / saved_self.image.name)