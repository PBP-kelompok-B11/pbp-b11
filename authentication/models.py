<<<<<<< HEAD
from django.contrib.auth.models import User
=======
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alamat = models.TextField()
    umur = models.PositiveIntegerField()
    nomor_handphone = models.CharField(max_length=20)

    def str(self):
        return self.user.username
>>>>>>> ad32ec64ac5e08c3c9ced140258fc6ce2b501355
