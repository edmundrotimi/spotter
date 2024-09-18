from api.serializers.book import AuthorListSerializer
from books.models import Book
from rest_framework import serializers


class BookSearchSerializer(serializers.ModelSerializer):
    author_id = message_sender = AuthorListSerializer()

    class Meta:
        model = Book
        fields = [
            'isbn', 'isbn13', 'language', 'average_rating', 'rating_dist', 'ratings_count', 'text_reviews_count',
            'publication_date', 'original_publication_date', 'format', 'edition_information', 'publisher', 'num_pages',
            'series_id', 'series_name', 'series_position', 'description', 'image_url', 'author_id'
        ]
