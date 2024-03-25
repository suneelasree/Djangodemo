
import csv
from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Load MovieLens ml-20m movies into the Movie model'

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            default="movies.csv",
            help="Path to the CSV file containing movies",
        )

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]

        with open(csv_file_path, newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Movie.objects.create(
                    movieId=row['movieId'],
                    title=row['title'],
                    genres=row['genres']
                )
        self.stdout.write(self.style.SUCCESS('Movies loaded successfully.'))
