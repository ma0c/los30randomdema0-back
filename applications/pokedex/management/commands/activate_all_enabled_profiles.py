from django.core.management.base import BaseCommand, CommandError
from applications.pokedex.models import Connection, Profile


class Command(BaseCommand):
    help = "Remove all connections"

    def handle(self, *args, **options):
        updated_rows = Profile.objects.filter(
            is_enabled=True,
        ).update(is_active=True)
        self.stdout.write(self.style.SUCCESS(f"Activating {updated_rows} profiles"))
