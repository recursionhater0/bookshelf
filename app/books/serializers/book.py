from rest_framework import serializers

from books.models import Book, BookCopy, Bookmark, Category, Review

from .authors import AuthorSerializer
from .generic import CreatedBySerializer


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "rating",
            "comment",
        )


class ReviewCreateSerializer(CreatedBySerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "book_copy",
            "rating",
            "comment",
            "created_by",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "is_active",
        )


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "authors",
            "categories",
        )


class BookDetailSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        model = Book
        fields = BookSerializer.Meta.fields + ("description",)


class BookCopySerializer(serializers.ModelSerializer):
    book = BookSerializer()
    is_bookmarked = serializers.BooleanField()

    class Meta:
        model = BookCopy
        fields = (
            "id",
            "book",
            "quantity",
            "cover_image",
            "average_rating",
            "is_bookmarked",
        )


class BookCopyDetailSerializer(BookCopySerializer):
    book = BookDetailSerializer()
    review = ReviewSerializer(source="ratings", many=True)

    class Meta(BookCopySerializer.Meta):
        model = BookCopy
        fields = BookCopySerializer.Meta.fields + (
            "isbn",
            "publication_date",
            "publisher",
            "review",
        )


class BookmarkSerializer(CreatedBySerializer):
    class Meta:
        model = Bookmark
        fields = (
            "created_by",
            "book_copy",
        )
