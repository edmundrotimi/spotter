from rest_framework import serializers

from core.api.utils.validate_image import clean_image
from core.books.models import Author, Book


class CreateBookSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(validators=[clean_image])

    class Meta:
        model = Book
        fields = [
            'title', 'isbn', 'isbn13', 'language', 'average_rating', 'rating_dist', 'ratings_count',
            'text_reviews_count', 'publication_date', 'original_publication_date', 'format', 'edition_information',
            'publisher', 'num_pages', 'series_id', 'series_name', 'series_position', 'description', 'image_url',
            'author_id', 'work_id'
        ]

    def create(self, validated_data):
        # request
        request = self.context.get('request')

        # Check if input data is valid
        serializer = self.__class__(data=validated_data)

        if serializer.is_valid():
            if request:

                # pop Many-to-Many fields
                work_data = validated_data.pop('work_id', None)
                author_data = validated_data.pop('author_id', None)

                # Continue with the normal creation process
                instance = Book.objects.create(**validated_data)

                # ensure popped data are not null
                if work_data is not None:
                    instance.work_id.set(work_data)
                if work_data is not None:
                    instance.author_id.set(author_data)
                return instance

            else:
                raise serializers.ValidationError('Invalid request.')
        else:
            raise serializers.ValidationError('Invalid inputs.')


class BookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'isbn13', 'language', 'average_rating', 'rating_dist', 'ratings_count',
            'text_reviews_count', 'publication_date', 'original_publication_date', 'format', 'edition_information',
            'publisher', 'num_pages', 'series_id', 'series_name', 'series_position', 'description', 'image_url',
            'author_id', 'work_id', 'asin'
        ]


class AuthorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = [
            'id', 'name', 'gender', 'image_url', 'about', 'fans_count', 'ratings_count', 'role', 'text_reviews_count',
            'book_ids', 'work_ids', 'works_count'
        ]


class CreateAuthorSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(validators=[clean_image])

    class Meta:
        model = Author
        fields = [
            'name', 'gender', 'image_url', 'about', 'fans_count', 'ratings_count', 'role', 'text_reviews_count',
            'book_ids', 'work_ids', 'works_count', 'average_rating'
        ]

    def create(self, validated_data):
        # request
        request = self.context.get('request')

        # Check if input data is valid
        serializer = self.__class__(data=validated_data)

        if serializer.is_valid():
            if request:
                # Extract Many-to-Many fields from validated_data
                books_data = validated_data.pop('book_ids', None)
                work_data = validated_data.pop('work_ids', None)

                # Continue with the normal creation process
                instance = Author.objects.create(**validated_data)

                # ensure popped data are not null
                if books_data is not None:
                    instance.book_ids.set(books_data)
                if work_data is not None:
                    instance.work_ids.set(work_data)
                return instance
            else:
                raise serializers.ValidationError('Invalid request.')
        else:
            raise serializers.ValidationError('Invalid inputs.')
