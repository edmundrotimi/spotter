from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Series, Work


class WorkAdmin(ModelAdmin):
    list_display = ['work_id', 'title', 'edition_id', 'user_position', 'books_count']
    list_display_links = ['work_id', 'edition_id', 'user_position', 'books_count']
    search_fields = ['work_id', 'title', 'edition_id', 'user_position', 'books_count']
    list_per_page = 100
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fields = ['work_id', 'title', 'edition_id', 'user_position', 'books_count']


class SeriesAdmin(ModelAdmin):
    list_display = ['id', 'title', 'series_works_count', 'primary_work_count', 'numbered']
    list_display_links = ['id', 'title', 'series_works_count', 'primary_work_count', 'numbered']
    search_fields = ['id', 'title', 'series_works_count', 'primary_work_count', 'numbered']
    list_per_page = 100
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fields = ['id', 'title', 'description', 'note', 'series_works_count', 'primary_work_count', 'numbered', 'works']


admin.site.register(Series, SeriesAdmin)
admin.site.register(Work, WorkAdmin)
