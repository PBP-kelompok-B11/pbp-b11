# events/models.py
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comments
from datetime import date
from django.contrib.auth.models import User

class Event(models.Model):
    LIGA = 'liga'
    TURNAMEN = 'turnamen'
    PERTANDINGAN = 'pertandingan'
    TIPE_CHOICES = [
        (LIGA, 'Liga'),
        (TURNAMEN, 'Turnamen'),
        (PERTANDINGAN, 'Pertandingan'),
    ]

    nama_event = models.CharField(max_length=100)
    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES)
    lokasi = models.CharField(max_length=100)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    comments = GenericRelation(Comments)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.nama_event

