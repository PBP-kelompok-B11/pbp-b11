import csv
from django.core.management.base import BaseCommand
from ibeth_clubs.models import Club, ClubRanking

class Command(BaseCommand):
    help = "Import clubs and rankings (with stadium & image URL) from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')
        parser.add_argument('--musim', type=str, default='2025/2026', help='Season name for ClubRanking')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        musim = options['musim']

        with open(csv_file, newline='', encoding='utf-8') as f:  # ubah ke utf-8 karena pakai simbol
            reader = csv.DictReader(f, delimiter=';')

            for row in reader:
                nama = row['Squad'].strip()
                negara = row['Country'].strip()

                # Ambil stadion dan url gambar kalau ada di CSV
                stadion = row.get('Stadion', 'Unknown Stadium').strip()
                tahun_berdiri = 1900  # default karena dataset tidak punya kolom tahun
                url_gambar = row.get('Url_Gambar', '').strip() or None

                # Buat atau update data club
                club, created = Club.objects.get_or_create(
                    nama=nama,
                    defaults={
                        'negara': negara,
                        'stadion': stadion,
                        'tahun_berdiri': tahun_berdiri,
                        'url_gambar': url_gambar,
                    }
                )

                if not created:
                    # Kalau club sudah ada, update data stadion & gambar-nya
                    club.negara = negara
                    club.stadion = stadion
                    club.url_gambar = url_gambar
                    club.save()
                    self.stdout.write(f'Updated club: {nama}')
                else:
                    self.stdout.write(self.style.SUCCESS(f'Created club: {nama}'))

                # Tambahkan ranking-nya
                peringkat = int(row['Rk'])
                ClubRanking.objects.update_or_create(
                    club=club,
                    musim=musim,
                    defaults={'peringkat': peringkat}
                )
                self.stdout.write(f'Ranking updated: {nama} - {musim} ({peringkat})')

        self.stdout.write(self.style.SUCCESS('CSV import finished successfully!'))
