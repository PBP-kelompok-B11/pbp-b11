# events/models.py
from django.db import models
from rafi_player.models import Player
from ibeth_clubs.models import Club
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comments
from datetime import date

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
    def __str__(self):
        return self.nama_event

