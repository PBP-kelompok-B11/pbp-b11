import pandas as pd
import json
from django.core.management.base import BaseCommand
from vidia_event.models import Event
from django.contrib.auth.models import User
from datetime import datetime

class Command(BaseCommand):
    help = "Import football matches from competitions.csv into Event model with team logos"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the competitions.csv file")
        parser.add_argument("logo_json", type=str, help="Path to the JSON file containing team logos")

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        logo_json_path = options["logo_json"]

        # Ambil user admin1
        try:
            admin_user = User.objects.get(username="admin1")
        except User.DoesNotExist:
            self.stderr.write("❌ User 'admin1' tidak ditemukan. Pastikan sudah ada di database.")
            return

        # Load JSON logo mapping
        with open(logo_json_path, "r") as f:
            logo_data = json.load(f)
        # Buat dict mapping nama tim → logo URL
        logo_map = {team["name"]: team["logo_file"] for team in logo_data}

        # Read CSV
        df = pd.read_csv(csv_path, quotechar='"')
        df.columns = df.columns.str.strip()
        last_col_name = df.columns[-1]
        print("Last column name:", repr(last_col_name))

        imported = 0

        for _, row in df.iterrows():
            try:
                tim_home = row.get("home_team_name") or ""
                tim_away = row.get("away_team_name") or ""
                lokasi = row.get(last_col_name) or ""

                # Ambil logo dari JSON, default "" jika tidak ada
                logo_home = logo_map.get(tim_home, "")
                logo_away = logo_map.get(tim_away, "")

                event = Event.objects.create(
                    created_by=admin_user,
                    tanggal=self.parse_date(row.get("date_GMT")),
                    tim_home=tim_home,
                    tim_away=tim_away,
                    skor_home=self.safe_int(row.get("home_team_goal_count")),
                    skor_away=self.safe_int(row.get("away_team_goal_count")),
                    nama_event=f"{tim_home} vs {tim_away}",
                    lokasi=lokasi,
                    logo_home=logo_home,
                    logo_away=logo_away
                )
                imported += 1
            except Exception as e:
                self.stderr.write(f"❌ Error importing row: {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {imported} matches."))

    # --- Helper methods ---
    def parse_date(self, date_str):
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
