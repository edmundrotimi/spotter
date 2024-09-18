from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Author, Book


class AuthorAdmin(ModelAdmin):
    list_display = ['id', 'name', 'gender', 'ratings_count', 'average_rating', 'text_reviews_count']
    list_display_links = ['id', 'ratings_count', 'average_rating', 'text_reviews_count']
    search_fields = ['id', 'name']
    list_per_page = 10
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fieldsets = [
        [
            'Bio',
            {
                'classes': ['wide', 'extrapretty'],
                'fields': ['id', 'name', 'gender', 'image_url', 'about'],
            },
        ],
        [
            'Ratings',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['ratings_count', 'average_rating', 'text_reviews_count', 'fans_count'],
            },
        ],
        [
            'Works',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['work_ids', 'works_count'],
            },
        ],
        [
            'Books',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['book_ids'],
            },
        ],
    ]


class BookAdmin(ModelAdmin):
    list_display = ['id', 'title', 'isbn']
    list_display_links = ['id', 'title', 'isbn']
    search_fields = ['id', 'title']
    list_per_page = 100
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fieldsets = [
        [
            'General Information',
            {
                'classes': ['wide', 'extrapretty'],
                'fields': ['id', 'title', 'isbn'],
            },
        ],
        [
            'Book Description',
            {
                'classes': ['wide', 'extrapretty'],
                'fields': ['num_pages', 'language', 'image_url', 'shelves', 'description'],
            },
        ],
        [
            'Author and Co-Author',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['authors'],
            },
        ],
        [
            'Works',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['work_ids'],
            },
        ],
        [
            'Book Number',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['isbn13', 'asin'],
            },
        ],
        [
            'Ratings',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['average_rating', 'rating_dist', 'ratings_count', 'text_reviews_count'],
            },
        ],
        [
            'Publication Info',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': [
                    'format', 'publication_date', 'original_publication_date', 'edition_information', 'publisher'
                ],
            },
        ],
        [
            'Series',
            {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['series_id', 'series_name', 'series_position'],
            },
        ],
    ]


# register admin settings
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
