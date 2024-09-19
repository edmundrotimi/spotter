# filters.py

import django_filters  # type: ignore
from django_filters.filters import Q

from core.books.models import Book


class BookFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_by_search_term')

    class Meta:
        model = Book
        exclude = [
            'title', 'id', 'isbn', 'isbn13', 'language', 'average_rating', 'rating_dist', 'ratings_count',
            'text_reviews_count', 'publication_date', 'original_publication_date', 'format', 'edition_information',
            'publisher', 'num_pages', 'series_id', 'series_name', 'series_position', 'description', 'image_url',
            'author_id', 'work_id', 'asin'
        ]

    def filter_by_search_term(self, queryset, name, value):
        # Perform filtering based on the search
        return queryset.filter(
            Q(id__icontains=value) | Q(title__icontains=value) | Q(isbn__icontains=value) |
            Q(isbn13__icontains=value) | Q(language__icontains=value) | Q(average_rating__icontains=value) |
            Q(rating_dist__icontains=value) | Q(ratings_count__icontains=value) |
            Q(text_reviews_count__icontains=value) | Q(publication_date__icontains=value) |
            Q(original_publication_date__icontains=value) | Q(format__icontains=value) |
            Q(edition_information__icontains=value) | Q(publisher__icontains=value) | Q(num_pages__icontains=value) |
            Q(series_id__icontains=value) | Q(series_name__icontains=value) | Q(series_position__icontains=value) |
            Q(description__icontains=value)
        )
