from django.contrib.auth.models import User
from django.db import models


class Route(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="trips")
  trip = models.JSONField()

  def __str__(self):
    return f"{self.user.username} ({self.trip['origin']['address']})"
