
import csv
from django.core.management.base import BaseCommand
from movies.models import Tag
from datetime import datetime

class Command(BaseCommand):
    help = 'Import tags from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', default="tags.csv", help='Path to the CSV file containing tags')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        self.stdout.write(self.style.SUCCESS(f'Starting import of tags from {csv_file_path}'))

        try:
            Tag.objects.all().delete()

            with open(csv_file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    Tag.objects.create(
                        userId=row['userId'],
                        movie_id=row['movieId'],
                        tag=row['tag'],
                        timestamp=datetime.utcfromtimestamp(int(row['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
                    )

            self.stdout.write(self.style.SUCCESS('Successfully imported tags'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing tags: {str(e)}'))