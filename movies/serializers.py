from rest_framework import serializers
from .models import Movie, Rating, Tag


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_genres(self, instance):
        return instance.genres.split("|")

    def get_tags(self, instance: Movie):
        tags = instance.tags.all()
        return ", ".join(tag.tag for tag in tags)

    class Meta:
        model = Movie
        fields = ["movieId", "title", "genres", "tags"]


class SubmitRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["rating"]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["userId", "movieId", "rating", "timestamp"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["userId", "movie", "tag", "timestamp"]