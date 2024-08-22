import argparse
import csv
import logging
import os

import django
from django.utils.crypto import get_random_string
from django.utils.text import slugify


LOGGER = logging.getLogger(__name__)

BADGES = [
    "Code",
    "Boxing",
    "Dancing",
    "Kosher",
    "Jiujitsy",
    "BF",
    "Literatura",
    "Corazon",
    "Hermanita",
    "Motos",
    "Memes",
    "Humor Negro",
    "Gatos",
    "Weed",
    "Alcohol",
    "Cafe",
    "Musica",
    "Medico",
    "Anime",
    "Viejos Amigos"
]

def load_pokedex_profiles(file: str):
    from applications.registration.models import PossibleAttendees
    from applications.pokedex.models import Badge, Profile

    badges_dict = {}

    for badge_name in BADGES:
        badge, created = Badge.objects.get_or_create(name=badge_name)
        if created:
            LOGGER.info(f"Badge {badge_name} created")
        badges_dict[badge_name] = badge

    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader):
            name, phone = row["Nombre Completo"], row["WP"]
            phone = phone.replace('"', "")
            possible_attendee = PossibleAttendees.objects.filter(phone=phone).all()
            if len(possible_attendee) == 0:
                LOGGER.error(f"Possible attendee for {name} not found, skipping")
                continue
            if len(possible_attendee) > 1:
                LOGGER.error(f"Multiple possible attendees for {name} found, skipping")
                continue
            possible_attendee = possible_attendee[0]
            profile, created = Profile.objects.get_or_create(attendee=possible_attendee)
            if created:
                LOGGER.info(f"Profile for {name} created")
            for badge_name in BADGES:
                if row[badge_name].strip():
                    badge = badges_dict[badge_name]
                    profile.badges.add(badge)
                    LOGGER.info(f"Badge {badge_name} added to {name}")

            if not profile.number:
                profile.number = index + 1
                profile.save()


if __name__ == "__main__":
    LOGGER.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.DEBUG)
    LOGGER.addHandler(logger_handler)
    parser = argparse.ArgumentParser(description="Load pokedex profiles to DB")
    parser.add_argument(
        "--file",
        type=str,
        help="The file to load the possible attendees from",
        required=True,
    )
    args = parser.parse_args()

    LOGGER.info(f"Loading possible attendees from {args.file}")

    LOGGER.debug(f"Configuring django app")


    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "los30randomdema0.settings")
    django.setup()
    LOGGER.debug(f"Django app configured")
    load_pokedex_profiles(args.file)