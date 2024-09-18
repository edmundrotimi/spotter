from core.books.models import Author, Book, BookFav  # type: ignore
from core.works.models import Series, Work  # type: ignore


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update({
        'books_counter': Book.objects.select_related('author_id', 'work_id').all().count(),
        'authors_counter': Author.objects.select_related('work_ids', 'book_ids').all().count(),
        'fav_counter': BookFav.objects.select_related('book').all().count(),
        'work_counter': Work.objects.all().count(),
        'Series_counter': Series.objects.select_related('works').all().count(),
    },)

    return context
