import pandas as pd
from django.core.management.base import BaseCommand
from vidia_event.models import Event
from datetime import datetime

class Command(BaseCommand):
    help = "Import football matches from competitions.csv into Event model"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the competitions.csv file")

    def handle(self, *args, **options):
        csv_path = options["csv_path"]

        # Read CSV safely — auto-detect separator
        df = pd.read_csv(csv_path, quotechar='"')
        last_col_name = df.columns[-1]  
        imported = 0

        for _, row in df.iterrows():
            try:
                tim_home = row.get("home_team_name") or ""
                tim_away = row.get("away_team_name") or ""
                lokasi = row.get(last_col_name) or ""
                event = Event.objects.create(
                    tanggal=self.parse_date(row.get("date_GMT")),
                    tim_home=tim_home,
                    tim_away=tim_away,
                    skor_home=self.safe_int(row.get("home_team_goal_count")),
                    skor_away=self.safe_int(row.get("away_team_goal_count")),
                    nama_event=f"{tim_home} vs {tim_away}",
                    lokasi = row.get(last_col_name) or ""
                )
                imported += 1
            except Exception as e:
                self.stderr.write(f"❌ Error importing row: {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {imported} matches."))

    # --- Helper methods ---
    def parse_date(self, date_str):
        """Convert 'Aug 10 2018 - 7:00pm' → datetime.date"""
        if pd.isna(date_str):
            return None
        try:
            return datetime.strptime(date_str, "%b %d %Y - %I:%M%p").date()
        except Exception:
            return None

    def safe_int(self, value):
        try:
            return int(value)
        except Exception:
            return None
