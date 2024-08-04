from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    members = models.ManyToManyField(User, related_name="treasure_groups")

    def __str__(self):
        return self.name
