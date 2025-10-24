from django.db import models

class Club(models.Model):
    nama = models.CharField(max_length=100)
    negara = models.CharField(max_length=100)
    stadion = models.CharField(max_length=100)
    tahun_berdiri = models.PositiveIntegerField()
    url_gambar = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nama


class ClubRanking(models.Model):
    club = models.ForeignKey(Club, related_name='rankings', on_delete=models.CASCADE)
    musim = models.CharField(max_length=20)
    peringkat = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.club.nama} - {self.musim} ({self.peringkat})"
