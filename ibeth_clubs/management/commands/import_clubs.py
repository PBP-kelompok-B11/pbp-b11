import csv
from django.core.management.base import BaseCommand
from ibeth_clubs.models import Club, ClubRanking

class Command(BaseCommand):
    help = "Import clubs and rankings from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')
        parser.add_argument('--musim', type=str, default='2025/2026', help='Season name for ClubRanking')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        musim = options['musim']

        with open(csv_file, newline='', encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                nama = row['Squad'].strip()
                negara = row['Country'].strip()

                # Contoh default stadion & tahun_berdiri karena CSV tidak punya info ini
                stadion = 'Unknown Stadium'
                tahun_berdiri = 1900

                club, created = Club.objects.get_or_create(
                    nama=nama,
                    defaults={'negara': negara, 'stadion': stadion, 'tahun_berdiri': tahun_berdiri}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Club created: {nama}'))
                else:
                    self.stdout.write(f'Club exists: {nama}')

                peringkat = int(row['Rk'])
                ClubRanking.objects.update_or_create(
                    club=club,
                    musim=musim,
                    defaults={'peringkat': peringkat}
                )
                self.stdout.write(f'Ranking updated: {nama} - {musim} ({peringkat})')

        self.stdout.write(self.style.SUCCESS('CSV import finished!'))
