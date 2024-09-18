import numpy as np

from core.api.utils.similarity import calculate_similarity
from core.books.models import Book, BookFav


def user_recommend_fav_books(rec_num=5):
    # Get all the books rated by the user
    favs = BookFav.objects.order_by('-fav_count')

    if not favs.exists():
        return []

    # Calculate similarity matrix for books
    similarity_matrix, titles = calculate_similarity()

    # Keep track of recommended books
    recommended_books = set()

    # Loop through the books  has rated highly
    for fav_rating in favs:
        book_favs = titles.index(fav_rating.book.title)
        similar_books_indices = np.argsort(similarity_matrix[book_favs])[::-1]

        # Get top_n similar books
        for idx in similar_books_indices[1:rec_num + 1]:  # Skip the first one (itself)
            similar_book_title = titles[idx]
            similar_book = Book.objects.get(title=similar_book_title)

            # Avoid recommending books the user has already rated
            if not BookFav.objects.filter(book=similar_book).exists():
                recommended_books.add(similar_book)

            if len(recommended_books) >= rec_num:
                break

    return list(recommended_books)
