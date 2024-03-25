from django.test import TestCase

# movies/tests.py
import pytest
from django.urls import reverse
from movies.models import Movie, Rating, Tag

@pytest.fixture
def sample_movie():
    return Movie.objects.create(
        movieId=1,
        title="Sample Movie",
        genres="Action|Adventure"
    )

@pytest.fixture
def sample_rating(sample_movie):
    return Rating.objects.create(
        userId=1,
        movieId=sample_movie,
        rating=4.5
    )

@pytest.fixture
def sample_tag(sample_movie):
    return Tag.objects.create(
        userId=1,
        movie=sample_movie,
        tag="Exciting",
        timestamp="2024-03-25 12:00:00"
    )

def test_movie_model(sample_movie):
    assert sample_movie.title == "Sample Movie"
    assert sample_movie.genres == "Action|Adventure"

def test_rating_model(sample_rating):
    assert sample_rating.userId == 1
    assert sample_rating.rating == 4.5

def test_tag_model(sample_tag):
    assert sample_tag.tag == "Exciting"

@pytest.mark.django_db
def test_movies_list_view(client):
    url = reverse("movies-list")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_movies_detail_view(client, sample_movie):
    url = reverse("movies-detail", args=[sample_movie.id])
    response = client.get(url)
    assert response.status_code == 200