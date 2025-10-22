from django.db import models

# Create your models here.
from django.db import models

class Player(models.Model):
    nama = models.CharField(max_length=100)
    negara = models.CharField(max_length=100)
    usia = models.PositiveIntegerField()
    tinggi = models.FloatField()
    berat = models.FloatField()
    posisi = models.CharField(max_length=50)

    def __str__(self):
        return self.nama


class CareerHistory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='riwayat_karier')
    klub = models.CharField(max_length=100)
    tahun_mulai = models.IntegerField()
    tahun_selesai = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.klub} ({self.tahun_mulai}-{self.tahun_selesai or 'Sekarang'})"


class SeasonStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='statistik_musim')
    musim = models.CharField(max_length=20)
    pertandingan = models.IntegerField()
    gol = models.IntegerField()
    assist = models.IntegerField()
    kartu = models.IntegerField()

    def __str__(self):
        return f"{self.player.nama} - {self.musim}"


class Achievement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='prestasi')
    deskripsi = models.CharField(max_length=200)
    tahun = models.IntegerField()

    def __str__(self):
        return f"{self.player.nama} - {self.deskripsi} ({self.tahun})"
