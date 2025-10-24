import csv
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rafi_player.models import Player, SeasonStats, CareerHistory, Achievement


class Command(BaseCommand):
    help = 'Import player dataset (CSV dengan delimiter ;) ke database Django'

    def handle(self, *args, **options):
        # Ganti path ke dataset kamu
        with open('datasets/2022-2023 Football Player Stats.csv', newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            user = User.objects.first()

            # --- fungsi bantu konversi aman ---
            def safe_int(value):
                try:
                    return int(float(value))
                except (ValueError, TypeError):
                    return 0

            for row in reader:
                # --- Data dasar ---
                nama = row.get('Player', '').strip()
                negara = row.get('Nation', '').strip()
                posisi = row.get('Pos', '').strip()
                usia = safe_int(row.get('Age'))

                # --- Player ---
                player, created = Player.objects.get_or_create(
                    nama=nama,
                    defaults={
                        'user': user,
                        'negara': negara,
                        'usia': usia,
                        'tinggi': 0.0,
                        'berat': 0.0,
                        'posisi': posisi,
                    }
                )

                # --- Season Stats ---
                musim = row.get('Comp', 'Unknown League')
                pertandingan = safe_int(row.get('MP'))
                gol = safe_int(row.get('Goals'))
                assist = safe_int(row.get('Assists'))

                SeasonStats.objects.create(
                    player=player,
                    musim=musim,
                    pertandingan=pertandingan,
                    gol=gol,
                    assist=assist,
                    kartu=0
                )

                # --- Career History ---
                CareerHistory.objects.create(
                    player=player,
                    klub=row.get('Squad', ''),
                    tahun_mulai=2024,
                    tahun_selesai=None
                )

                # --- Achievement ---
                if gol >= 15:
                    Achievement.objects.create(
                        player=player,
                        deskripsi="Top Scorer",
                        tahun=2024
                    )
                elif assist >= 10:
                    Achievement.objects.create(
                        player=player,
                        deskripsi="Playmaker of the Season",
                        tahun=2024
                    )
                else:
                    Achievement.objects.create(
                        player=player,
                        deskripsi="Professional Player",
                        tahun=2024
                    )

            self.stdout.write(self.style.SUCCESS('✅ Data pemain berhasil diimpor!'))
