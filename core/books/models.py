from django.contrib.auth import get_user_model
from django.db import models
from shortuuid.django_fields import ShortUUIDField

from core.works.models import Work

User = get_user_model()


class Author(models.Model):
    id = ShortUUIDField(length=30, max_length=40, alphabet='16777216', primary_key=True)  # noqa: A003
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(max_length=2000, null=True, blank=True)
    fans_count = models.IntegerField()
    ratings_count = models.IntegerField()
    average_rating = models.IntegerField()
    role = models.CharField(max_length=300, null=True, blank=True)
    text_reviews_count = models.IntegerField()
    book_ids = models.ManyToManyField('Book')
    work_ids = models.ManyToManyField(Work)
    works_count = models.IntegerField()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    id = ShortUUIDField(length=8, max_length=40, alphabet='123876', primary_key=True)  # noqa: A003
    title = models.CharField(max_length=300)
    author_id = models.ManyToManyField('Author')
    work_id = models.ManyToManyField(Work)
    isbn = models.CharField(max_length=200)
    isbn13 = models.CharField(max_length=200)
    asin = models.CharField(max_length=200)
    language = models.CharField(max_length=50)
    average_rating = models.FloatField(max_length=50)
    rating_dist = models.CharField(max_length=300)
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    publication_date = models.CharField(max_length=100)
    original_publication_date = models.CharField(max_length=100)
    format = models.CharField(max_length=100)  # noqa: A003
    edition_information = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    num_pages = models.IntegerField()
    series_id = models.CharField(max_length=100)
    series_name = models.CharField(max_length=300)
    series_position = models.CharField(max_length=100)
    description = models.TextField(max_length=4000)

    def __str__(self):
        return f'{self.id}'


class BookFav(models.Model):
    id = ShortUUIDField(length=30, max_length=40, alphabet='12ge76', primary_key=True)  # noqa: A003
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    fav_count = models.IntegerField(help_text='total number of fav for a book')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Book Fav'
        verbose_name_plural = 'Book Fav'
