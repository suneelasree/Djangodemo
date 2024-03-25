# movies/management/commands/import_ratings.py
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from movies.models import Rating


class Command(BaseCommand):
    help = "Import ratings from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            default="ratings.csv",
            help="Path to the CSV file containing ratings",
        )

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]

        self.stdout.write(
            self.style.SUCCESS(f"Starting import of ratings from {csv_file_path}")
        )

        try:
            Rating.objects.all().delete()
            with open(csv_file_path, "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    Rating.objects.create(
                        userId=row["userId"],
                        movieId=row["movieId"],
                        rating=row["rating"],
                        timestamp=datetime.utcfromtimestamp(int(row['timestamp']))
                    )

            self.stdout.write(self.style.SUCCESS("Successfully imported ratings"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing ratings: {str(e)}"))