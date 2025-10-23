# events/models.py
from django.db import models
from rafi_player.models import Player
from clubs.models import Club
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

    def __str__(self):
        return self.nama_event


class EventParticipation(models.Model):
    PERAN_CHOICES = [
        ('pemain', 'Pemain'),
        ('kapten', 'Kapten'),
        ('klub', 'Klub'),
    ]

    HASIL_CHOICES = [
        ('menang', 'Menang'),
        ('kalah', 'Kalah'),
        ('juara', 'Juara'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)
    peran = models.CharField(max_length=20, choices=PERAN_CHOICES)
    hasil = models.CharField(max_length=20, choices=HASIL_CHOICES)

    def __str__(self):
        if self.player:
            return f"{self.player.name} - {self.event.nama_event}"
        elif self.club:
            return f"{self.club.name} - {self.event.nama_event}"
        return f"{self.event.nama_event}"
