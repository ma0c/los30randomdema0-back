from django.core.management.base import BaseCommand, CommandError
from applications.pokedex.models import Connection


class Command(BaseCommand):
    help = "Remove all connections"

    def handle(self, *args, **options):
        Connection.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All connections removed"))
