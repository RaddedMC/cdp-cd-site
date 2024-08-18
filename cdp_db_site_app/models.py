from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from cdp_db_site import settings


# Disc group as defined in the player.
class Group(models.Model):
    title = models.CharField(max_length=200)
    color = ColorField(format="hex")
    def __str__(self):
        return f"Group #{self.id}: {self.title}"

    def as_json(self):
        return {"id": self.id, "title": self.title, "color": self.color}


# Disc in the player
class Disc(models.Model):
    position = models.PositiveSmallIntegerField(primary_key=True,
                                                validators=[MinValueValidator(1), MaxValueValidator(settings.CDP_SIZE)])
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)
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