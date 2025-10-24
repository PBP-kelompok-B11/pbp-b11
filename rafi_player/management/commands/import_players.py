import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rafi_player.models import Player, SeasonStats, CareerHistory, Achievement

class Command(BaseCommand):
    help = 'Import player dataset (CSV dengan delimiter ;) ke database Django'

    def handle(self, *args, **options):
        # --- Pastikan ada user untuk assign Player ---
        user, created = User.objects.get_or_create(
            username='admin_import',
            defaults={'email': 'admin@example.com', 'password': 'pbp1234'}
        )
        if created:
            user.set_password('pbp1234')
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ User default dibuat: admin_import / pbp1234'))

        # --- Buka CSV ---
        with open('datasets/2022-2023 Football Player Stats.csv', newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            # Fungsi bantu konversi angka
            def safe_int(value):
                try:
                    return int(float(value))
                except (ValueError, TypeError):
                    return 0

            def safe_float(value):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return 0.0

            for row in reader:
                nama = row.get('Player', '').strip()
                if not nama:
                    continue  # Skip kalau nama kosong

                negara = row.get('Nation', '').strip()
                posisi = row.get('Pos', '').strip()
                usia = safe_int(row.get('Age'))
                tinggi = safe_float(row.get('Height'))
                berat = safe_float(row.get('Weight'))
                thumbnail = (row.get('Thumbnail') or '').strip()

                # --- Player ---
                player, created = Player.objects.get_or_create(
                    nama=nama,
                    defaults={
                        'user': user,
                        'negara': negara,
                        'usia': usia,
                        'tinggi': tinggi,
                        'berat': berat,
                        'posisi': posisi,
                        'thumbnail': thumbnail,
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
                klub = row.get('Squad', '').strip()
                if klub:
                    CareerHistory.objects.create(
                        player=player,
                        klub=klub,
                        tahun_mulai=2024,
                        tahun_selesai=None
                    )

                # --- Achievement ---
                if gol >= 15:
                    desc = "Top Scorer"
                elif assist >= 10:
                    desc = "Playmaker of the Season"
                else:
                    desc = "Professional Player"

                Achievement.objects.create(
                    player=player,
                    deskripsi=desc,
                    tahun=2024
                )

            self.stdout.write(self.style.SUCCESS('✅ Data pemain berhasil diimpor!'))
