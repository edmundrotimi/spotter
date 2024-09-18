from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from core.books.models import Book


# Function to calculate book similarity based on genres
def calculate_similarity():
    books = Book.objects.all()
    titles = [book.title for book in books]

    # Convert genres into a matrix of token counts
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','))
    title_matrix = vectorizer.fit_transform(titles)

    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(title_matrix)

    return similarity_matrix, titles
