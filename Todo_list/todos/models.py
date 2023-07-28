from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(default='')
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # represents the class object as a string (title).if str is not used then pointer of the string is described
        return self.title
