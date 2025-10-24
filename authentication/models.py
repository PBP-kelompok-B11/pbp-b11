# authentication/models.py
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alamat = models.TextField()
    umur = models.PositiveIntegerField()
    nomor_handphone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

