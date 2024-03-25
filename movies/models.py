# movies/models.py
from django.db import models


class Movie(models.Model):
    movieId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)  # Assuming genres are stored as a string

    def __str__(self):
        return f"{self.movieId}: {self.title}"


class Rating(models.Model):
    userId = models.IntegerField()
    movieId = models.IntegerField()
    rating = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.userId} rated {self.movieId} with {self.rating}"


class Tag(models.Model):
    userId = models.IntegerField()
    movie = models.ForeignKey(
        Movie, db_column="movieId", on_delete=models.CASCADE, related_name="tags"
    )
    tag = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.userId} tagged {self.movieId} with '{self.tag}'"