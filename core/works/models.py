from django.db import models
from shortuuid.django_fields import ShortUUIDField


class Work(models.Model):
    work_id = ShortUUIDField(length=30, max_length=40, alphabet='2467422', primary_key=True)
    title = models.CharField(max_length=200)
    edition_id = models.CharField(max_length=200)
    user_position = models.CharField(max_length=200, null=True, blank=True)
    books_count = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.work_id}'

    class Meta:
        verbose_name = 'Works'
        verbose_name_plural = 'Works'


class Series(models.Model):
    id = ShortUUIDField(length=30, max_length=40, alphabet='40323', primary_key=True)  # noqa: A003
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=4000, null=True, blank=True)
    note = models.TextField(max_length=4000, null=True, blank=True)
    series_works_count = models.CharField(max_length=200)
    primary_work_count = models.CharField(max_length=200)
    numbered = models.CharField(max_length=200)
    works = models.ManyToManyField('Work')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = 'Series'
