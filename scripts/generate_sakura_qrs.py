import argparse
import csv
import logging
import qrcode


LOGGER = logging.getLogger(__name__)


def generate_qrs(file: str, output_folder: str):
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader):
            index, qr = row["ID"], row["Slug"]
            img = qrcode.make(qr)
            output_file = f"{output_folder}/{index}-{qr}.png"
            LOGGER.info(f"Generating QR for {index} with slug {qr}")
            img.save(output_file)
            LOGGER.info(f"QR saved to {output_file}")


if __name__ == "__main__":
    LOGGER.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.DEBUG)
    LOGGER.addHandler(logger_handler)
    parser = argparse.ArgumentParser(description="Generate Sakura QRs")
    parser.add_argument(
        "--file",
        type=str,
        help="The file to load the possible attendees from",
        required=True,
    )
    parser.add_argument(
        "--output_folder",
        default="sakura_qrs",
        type=str,
        help="The file to load the possible attendees from",
        required=True,
    )
    args = parser.parse_args()

    generate_qrs(args.file, args.output_folder)
