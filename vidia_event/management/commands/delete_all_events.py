from django.core.management.base import BaseCommand
from vidia_event.models import Event

class Command(BaseCommand):
    help = "Delete all events from the Event model"

    def handle(self, *args, **options):
        count = Event.objects.count()
        if count == 0:
            self.stdout.write(self.style.WARNING("⚠️ No events to delete."))
            return

        Event.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully deleted all {count} events."))
