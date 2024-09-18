from django.urls import path

from .views import (
    AddFavBookRecommendation, AllAuthorListings, AllBooksListings, AuthorSingleByID, BookSingleByID, CreateAuthor,
    CreateBook, DeleteAuthorListing, DeleteBookListing, LoginAPIView, RemoveFavBookRecommendation, UpdateAuthor,
    UpdateBook
)

urlpatterns = [

    # user login attempts
    path('login/', LoginAPIView.as_view(), name='user_login'),
    # book
    path('book/create/', CreateBook.as_view(), name='api_book_create'),
    path('book/update/<int:id>', UpdateBook.as_view(), name='api_book_update'),
    path('books/all/', AllBooksListings.as_view(), name='api_books_all'),
    path('book/<int:id>/', BookSingleByID.as_view(), name='api_book_single'),
    path('book/delete/<int:id>', DeleteBookListing.as_view(), name='api_book_single'),
    # author
    path('author/create/', CreateAuthor.as_view(), name='api_author_create'),
    path('author/update/<int:id>', UpdateAuthor.as_view(), name='api_author_update'),
    path('authors/all/', AllAuthorListings.as_view(), name='api_authors_all'),
    path('author/<int:id>/', AuthorSingleByID.as_view(), name='api_author_single'),
    path('author/delete/<int:id>', DeleteAuthorListing.as_view(), name='api_author_single'),
    # recommendation
    path('fav/book/add/<int:id>', AddFavBookRecommendation.as_view(), name='api_book_fav_add'),
    path('fav/book/remove/<int:id>', RemoveFavBookRecommendation.as_view(), name='api_book_fav_remove'),
]
