from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comments
from django.contrib.auth.models import User
from datetime import date

class Event(models.Model):
    
    nama_event = models.CharField(max_length=100)  # Name of the event (e.g., Premier League)
    lokasi = models.CharField(max_length=100)
    tanggal = models.DateField(default=date.today)

    # New fields based on spreadsheet
    tim_home = models.CharField(max_length=100, null=True, blank=True)
    tim_away = models.CharField(max_length=100, null=True, blank=True)
    skor_home = models.PositiveIntegerField(null=True, blank=True)
    skor_away = models.PositiveIntegerField(null=True, blank=True)

    comments = GenericRelation(Comments)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.tim_home} vs {self.tim_away} ({self.nama_event})"
