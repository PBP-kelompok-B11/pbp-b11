from django.core.management.base import BaseCommand
from django.conf import settings
import json
import os

from ibeth_clubs.models import Club


class Command(BaseCommand):
    help = "Load clubs and attach local logo PNGs"

    def handle(self, *args, **options):
        BASE_DIR = settings.BASE_DIR

        JSON_PATH = BASE_DIR / 'vidia_event/data/logo_club.json'
        LOGO_BASE_PATH = BASE_DIR / 'vidia_event/data/logos'

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

            filename = os.path.basename(item['logo_file'])
            logo_path = LOGO_BASE_PATH / filename

            if logo_path.exists():
                # path yang dikirim ke Flutter (relative)
                club.url_gambar = f"/{logo_path.relative_to(BASE_DIR)}"
                club.save()
            else:
                self.stdout.write(
                    self.style.WARNING(f"Logo not found: {logo_path}")
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"[{'Created' if created else 'Updated'}] {club.nama}"
                )
            )
