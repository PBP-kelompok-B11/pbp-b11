from django.db import models

class Club(models.Model):
    nama = models.CharField(max_length=100)
    negara = models.CharField(max_length=100)
    stadion = models.CharField(max_length=100)
    tahun_berdiri = models.PositiveIntegerField()

    def __str__(self):
        return self.nama


class ClubRanking(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='rankings')
    musim = models.CharField(max_length=50)
    peringkat = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.club.nama} - {self.musim}: {self.peringkat}"
