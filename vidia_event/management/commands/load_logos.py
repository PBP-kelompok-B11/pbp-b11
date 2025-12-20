from django.core.management.base import BaseCommand
from django.conf import settings
import json
import os

from ibeth_clubs.models import Club

class Command(BaseCommand):
    help = "Load clubs and attach local logo PNGs"

    def handle(self, *args, **options):
        BASE_DIR = settings.BASE_DIR

        # 1. Pastikan path ke JSON benar
        JSON_PATH = BASE_DIR / 'vidia_event/data/logo_club.json'

        if not JSON_PATH.exists():
            self.stdout.write(self.style.ERROR(f"JSON file not found at {JSON_PATH}"))
            return

        with open(JSON_PATH) as f:
            data = json.load(f)

        for item in data:
            club, created = Club.objects.get_or_create(
                nama=item['name'],
                defaults={
                    'negara': 'England',
                    'stadion': '-',
                    'tahun_berdiri': 0
                }
            )

            # 2. Ambil path dari JSON (misal: "static/logos/arsenal.png")
            # Sesuaikan key-nya, apakah 'logo_file' atau 'logo_url' di JSON kamu
            relative_logo_path = item.get('logo_file') or item.get('logo_url')

            if relative_logo_path:
                # 3. Gabungkan dengan BASE_DIR untuk cek fisik file
                # Path fisik: /Users/vidia/.../pbp-b11/static/logos/arsenal.png
                full_logo_path = BASE_DIR / relative_logo_path.lstrip('/')

                if full_logo_path.exists():
                    # 4. Simpan ke database dengan garis miring di depan agar terbaca sebagai URL
                    # Hasil: /static/logos/arsenal.png
                    path_for_db = f"/{relative_logo_path.lstrip('/')}"
                    club.url_gambar = path_for_db
                    club.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f"[{'Created' if created else 'Updated'}] {club.nama} -> {path_for_db}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Logo not found at: {full_logo_path}")
                    )
            else:
                self.stdout.write(self.style.WARNING(f"No logo path defined for {item['name']}"))