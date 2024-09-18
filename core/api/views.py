from django.db.models import F
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from core.api.auth_login import LoginSerializer
from core.api.filters.book import BookFilter
from core.api.serializers.book import (
    AuthorListSerializer, BookListSerializer, CreateAuthorSerializer, CreateBookSerializer
)
from core.api.serializers.search.book_search import BookSearchSerializer
from core.api.service import APIService
from core.api.utils.recommendations import user_recommend_fav_books
from core.books.models import Author, Book, BookFav


class LoginAPIView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        # init serializer
        serializer = LoginSerializer(data=request.data)

        # check if serializer is valid
        if serializer.is_valid():
            # get user input
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # authenticate user
            user = APIService.auth_login_user(self.request, email, password)

            if user is None:
                # Process the data here
                response_data = {
                    'login_message': 'Invalid login credentials.',
                    'attempt_left': APIService.get_access_attempts(self.request),
                }
            else:
                # token
                refresh = RefreshToken.for_user(user)
                # Process the data here
                response_data = {
                    'login_message': 'Login successful.',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'attempt_left': APIService.get_access_attempts(self.request),
                }

            return Response(response_data, status=status.HTTP_200_OK)

        # response
        return Response({'detail': 'Invalid credentials. Use valid credentials for email and password.'},
                        status=status.HTTP_401_UNAUTHORIZED)


class CreateBook(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    serializer_class = CreateBookSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class UpdateBook(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        # get id
        instance_id = self.kwargs.get('id')

        if Book.objects.filter(id=instance_id).exists():
            return super().update(request, *args, **kwargs)
        else:
            # response
            return Response({'detail': 'Record does not else'}, status=status.HTTP_400_BAD_REQUEST)


class AllBooksListings(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    serializer_class = BookSearchSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilter


class BookSingleByID(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    lookup_field = 'id'

    def get_object(self):
        try:
            # get rerecord
            return super().get_object()
        except Book.DoesNotExist:
            # raise a NotFound exception
            raise NotFound(detail='The book with the given ID was not found.')


class DeleteBookListing(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    serializer_class = AllBooksListings
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # init message
        message = {'detail': 'Record does not else'}
        status_code = status.HTTP_400_BAD_REQUEST

        if Book.objects.filter(id=self.kwargs['id']).exists():
            instance = self.get_object(id=self.kwargs['id'])
            self.perform_destroy(instance)
            message['detail'] = 'Book deleted successfully'
            status_code = status.HTTP_200_OK

        # response
        return Response(message, status=status_code)


class CreateAuthor(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Author.objects.all()
    serializer_class = CreateAuthorSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class UpdateAuthor(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        # get id
        instance_id = self.kwargs.get('id')

        if Author.objects.filter(id=instance_id).exists():
            return super().update(request, *args, **kwargs)
        else:
            # response
            return Response({'detail': 'Record does not else'}, status=status.HTTP_400_BAD_REQUEST)


class AllAuthorListings(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = [IsAuthenticated]


class AuthorSingleByID(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    lookup_field = 'id'

    def get_object(self):
        try:
            # return record
            return super().get_object()
        except Author.DoesNotExist:
            # raise a NotFound exception
            raise NotFound(detail='The author with the given ID was not found.')


class DeleteAuthorListing(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # init message
        message = {'detail': 'Record does not else'}
        status_code = status.HTTP_400_BAD_REQUEST

        # check if author exist
        if Author.objects.filter(id=self.kwargs['id']).exists():
            # get id
            instance = self.get_object(id=self.kwargs['id'])
            # delete record
            self.perform_destroy(instance)
            # update response message
            message['detail'] = 'Record deleted successfully'
            status_code = status.HTTP_200_OK

        # response
        return Response(message, status=status_code)


class AddFavBookRecommendation(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = BookSingleByID.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AllBooksListings

    def get_queryset(self):
        # get id from request
        book_id = self.kwargs.get('id')

        if Book.objects.filter(id=book_id).exists():
            # get book
            get_book = Book.objects.get(id=book_id)

            # create and update fields
            BookFav.objects.update_or_create(
                book=get_book,
                defaults={'fav_count': F('count') + 1}  # update field if it exist or set on creation
            )

            # fav book does not exist
            recommended_books = user_recommend_fav_books(top_n=5)
            return recommended_books
        else:
            # book does not exist
            return Response({'detail': 'Record does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFavBookRecommendation(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = BookSingleByID.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AllBooksListings

    def get_queryset(self):
        # Access 'id' from the request
        book_id = self.kwargs.get('id')

        # check if the book exist
        if Book.objects.filter(id=book_id).exists():
            # get book
            get_book = Book.objects.get(id=book_id)

            # check if the fav book record exist
            if BookFav.objects.filter(book=get_book).exists():
                # delete record
                BookFav.objects.delete(book=get_book)

                # Get the recommended books
                recommended_books = user_recommend_fav_books(rec_num=5)
                # return recommendation as a list
                return recommended_books
            else:
                # fav book does not exist
                return Response({'detail': 'Record does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # book does not exist
            return Response({'detail': 'Record does not exist'}, status=status.HTTP_400_BAD_REQUEST)
