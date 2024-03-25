# movies/management/commands/export_movies.py
import csv
from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Export MovieLens movie list'

    def handle(self, *args, **kwargs):
        filename = 'movie_list.csv'  # Output file name
        queryset = Movie.objects.all()  # Get all movies

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Movie ID', 'Title', 'Genres'])  # Write header row

            for movie in queryset:
                writer.writerow([movie.movieId, movie.title, movie.genres])  # Write movie data
