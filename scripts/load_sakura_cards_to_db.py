import argparse
import csv
import logging
import os

import django
from django.utils.crypto import get_random_string
from django.utils.text import slugify


LOGGER = logging.getLogger(__name__)


def load_sakura_cards(file: str):
    from applications.sakura.models import Question
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader):
            id_, question, answer, theme, responsible, evaluation_type, slug = row["ID"], row["Pregunta"], row["Respuesta"], row["Tematica"], row["Responsable"], row["Repuesta tipo"], row["Slug"]
            LOGGER.info(f"Creating Sakura card {id_}, {theme}, {slug}")
            question, created = Question.objects.get_or_create(
                serial_number=id_,
                question=question,
                answer=answer,
                theme=theme,
                responsible=responsible,
                evaluation_type=evaluation_type,
                slug=slug,
            )


if __name__ == "__main__":
    LOGGER.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.DEBUG)
    LOGGER.addHandler(logger_handler)
    parser = argparse.ArgumentParser(description="Load sakura cards to the database")
    parser.add_argument(
        "--file",
        type=str,
        help="The file to load the sakura cards from",
        required=True,
    )
    args = parser.parse_args()

    LOGGER.info(f"Loading sakura cards from {args.file}")

    LOGGER.debug(f"Configuring django app")


    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "los30randomdema0.settings")
    django.setup()
    LOGGER.debug(f"Django app configured")
    load_sakura_cards(args.file)
