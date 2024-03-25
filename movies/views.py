from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Rating, Tag
from .serializers import MovieSerializer, RatingSerializer, SubmitRatingSerializer, TagSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.filters import OrderingFilter


class MoviePagination(PageNumberPagination):
    page_size = 10  # Set the number of movies per page

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission class to allow read-only access for anonymous users.
    """

    def has_permission(self, request, view):
        return (
            request.method in ["GET", "HEAD", "OPTIONS"]
            or request.user
            and request.user.is_authenticated
        )


class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = "movieId"
    pagination_class = MoviePagination
    filter_backends = [OrderingFilter]  # Enable ordering filter

    # Define ordering fields
    ordering_fields = ['title', 'release_date']  # Add 'release_date' if applicable

    # Optionally, set a default ordering
    ordering = ['title']  # Default ordering by title
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="genre",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter movies by genre",
            ),
            openapi.Parameter(
                name="title",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter movies by title",
            ),
            openapi.Parameter(
                name="tag",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter movies by tag",
            ),
            openapi.Parameter(
                "movieId",
                openapi.IN_PATH,
                description="ID of the movie",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "rating",
                openapi.IN_QUERY,
                description="Rating value (between 0.5 and 5)",
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT
            ),
            openapi.Parameter(
                "genre",
                openapi.IN_QUERY,
                description="Genre of the movie",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "tag",
                openapi.IN_QUERY,
                description="Tag related to the movie",
                type=openapi.TYPE_STRING
            ),
        ],
    )

    @action(detail=True, methods=['GET'])
    def movie_by_id(self, request, pk=None):
        try:
            movie = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)

    @swagger_auto_schema(
        methods=['post'],
        request_body=MovieSerializer,
        responses={201: 'Movie created successfully', 400: 'Invalid data'},
        operation_summary='Create movie',
        operation_description='Creates a new movie.'
    )
    # Create a new movie
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        methods=['put'],
        request_body=MovieSerializer,
        responses={200: 'Movie updated successfully', 400: 'Invalid data'},
        operation_summary='Update movie',
        operation_description='Updates an existing movie.'
    )
    def update(self, request, pk=None):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = self.serializer_class(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        methods=['patch'],
        request_body=MovieSerializer,
        responses={200: 'Movie partially updated successfully', 400: 'Invalid data'},
        operation_summary='Partial update movie',
        operation_description='Partially updates an existing movie.'
    )
    # Partial update of a movie
    def partial_update(self, request, pk=None):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = self.serializer_class(movie, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        methods=['get'],
        responses={200: MovieSerializer(many=True)},
        operation_summary='List movies',
        operation_description='Retrieves a paginated list of all movies.'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.query_params.get("genre", None)

        if genre:
            # Filter movies based on the provided genre
            queryset = queryset.filter(genres__icontains=genre)

        tag = self.request.query_params.get("tag", None)

        if tag:
            # Filter movies based on the provided tag
            queryset = queryset.filter(tags__tag__icontains=tag)

        return queryset

    @swagger_auto_schema(
        methods=['post'],
        request_body=SubmitRatingSerializer,
        responses={201: 'Rating added successfully', 400: 'Invalid rating value or already rated'},
        operation_summary='Rate a movie',
        operation_description='Allows an authenticated user to rate a movie with a value between 0.5 and 5.'
    )
    @swagger_auto_schema(
        methods=['post'],
        request_body=SubmitRatingSerializer,
        responses={201: 'Rating added successfully', 400: 'Invalid rating value or already rated'},
        operation_summary='Rate a movie',
        operation_description='Allows an authenticated user to rate a movie with a value between 0.5 and 5.'
    )
    @action(detail=True, methods=["POST"])
    def rate(self, request, movieId=None):
        movie = self.get_object()
        user = request.user  # Assumes authentication is set up

        # Check if the user has already rated the movie
        existing_rating = Rating.objects.filter(movie=movie, user=user).first()

        if existing_rating:
            return Response(
                {"detail": "You have already rated this movie."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate the rating value
        rating_value = request.data.get("rating")
        if rating_value is None or not (0.5 <= rating_value <= 5):
            return Response(
                {"detail": "Invalid rating value. It must be between 0.5 and 5."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new rating for the movie
        rating_data = {"user": user.id, "movie": movie.movieId, "rating": rating_value}
        serializer = RatingSerializer(data=rating_data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Rating added successfully."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = "movieId"
    pagination_class = MoviePagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "tagId"
    pagination_class = MoviePagination