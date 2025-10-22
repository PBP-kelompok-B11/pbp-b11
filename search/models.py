from django.db import models
from django.contrib.auth.models import User

class SearchQuery(models.Model):
    JENIS_PILIHAN = [
        ('pemain', 'Pemain'),
        ('klub', 'Klub'),
    ]

    # User bisa kosong (karena fitur search bisa diakses tanpa login)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    kata_kunci = models.CharField(max_length=100)
    jenis = models.CharField(max_length=10, choices=JENIS_PILIHAN)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_str = self.user.username if self.user else "Anonim"
        return f"{user_str} mencari '{self.kata_kunci}' ({self.jenis})"

    class Meta:
        ordering = ['-tanggal']
        verbose_name_plural = "Search Queries"
