from django.db import models
from django.contrib.auth.models import User


class Notesmodel(models.Model):

    id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=500, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.description)

