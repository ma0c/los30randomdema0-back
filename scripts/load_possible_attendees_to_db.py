import argparse
import csv
import logging
import os

import django
from django.utils.crypto import get_random_string
from django.utils.text import slugify


LOGGER = logging.getLogger(__name__)


def load_possible_attendees(file: str):
    from applications.registration.models import PossibleAttendees
    with open(file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            name, instagram, phone = row[0], row[1], row[2]
            phone = phone.replace('"', "")
            slug = slugify(f"{name}-{get_random_string(4)}")
            if name and phone and instagram:
                LOGGER.info(f"Creating possible attendee {name}, {phone}, {instagram}, {slug}")
                PossibleAttendees.objects.create(
                    name=name,
                    phone=phone,
                    slug=slug,
                    instagram=instagram,
                )


if __name__ == "__main__":
    LOGGER.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.DEBUG)
    LOGGER.addHandler(logger_handler)
    parser = argparse.ArgumentParser(description="Load possible attendees to the database")
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
    load_possible_attendees(args.file)
