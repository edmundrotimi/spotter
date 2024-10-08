from django.db.models import F, Q
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from core.api.auth_login import LoginSerializer
from core.api.filters.book import BookFilter
from core.api.serializers.book import (
    AuthorListSerializer, BookListSerializer, CreateAuthorSerializer, CreateBookSerializer
)
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
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        # get id
        instance = self.get_object()

        # pop data for many to many
        work_data = request.pop('work_id', None)
        author_data = request.pop('author_id', None)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # ensure popped data are not null
        if author_data is not None:
            instance.author_id(author_data)
        if work_data is not None:
            instance.work_ids.set(work_data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBooksListings(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
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
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # init message
        message = {'detail': 'Record does not else'}
        status_code = status.HTTP_400_BAD_REQUEST

        if Book.objects.filter(id=self.kwargs['id']).exists():
            Book.objects.filter(id=self.kwargs['id']).delete()
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
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        # Get the instance to be updated
        instance = self.get_object()

        # Extract many to many field from the request data
        work_data = request.data.pop('work_ids', None)
        book_data = request.data.pop('book_ids', None)

        # save record
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # ensure popped data are not null
        if book_data is not None:
            instance.book_ids.set(book_data)
        if work_data is not None:
            instance.work_ids.set(work_data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AllAuthorListings(generics.ListAPIView):
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
            # delete record
            Author.objects.filter(id=self.kwargs['id']).delete()
            # update response message
            message['detail'] = 'Record deleted successfully'
            status_code = status.HTTP_200_OK

        # response
        return Response(message, status=status_code)


class AddFavBookRecommendation(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BookListSerializer

    def get(self, request, *args, **kwargs):
        # get id from request
        book_id = self.kwargs.get('id')

        if Book.objects.filter(id=book_id):
            # get book
            get_book = Book.objects.get(id=book_id)

            # update field if it exist or set on creation
            if BookFav.objects.filter(Q(book=get_book) & ~Q(user=self.request.user)).exists():
                BookFav.objects.update(book=get_book, fav_count=F('fav_count') + 1)
            elif not BookFav.objects.filter(Q(book=get_book)):
                BookFav.objects.create(user=self.request.user, book=get_book, fav_count=1)

            # fav book does not exist
            recommended_books = user_recommend_fav_books(rec_num=5, title=get_book.title)

            # Serialize the recommended books
            serializer = BookListSerializer(recommended_books, many=True)

            return Response({'recommendations': serializer.data}, status=status.HTTP_200_OK)
        else:
            # book does not exist
            return Response({'detail': 'Record does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFavBookRecommendation(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BookListSerializer

    def get(self, request, *args, **kwargs):
        # Access 'id' from the request
        book_id = self.kwargs.get('id')

        try:
            # get book
            get_book = Book.objects.get(id=book_id)

            BookFav.objects.filter(book__id=get_book.id).delete()

            # fav book does not exist
            return Response({'detail': 'Record removed from fav list'}, status=status.HTTP_200_OK)

        except Exception:
            return Response({'detail': 'Record is not in fav list'}, status=status.HTTP_404_NOT_FOUND)
