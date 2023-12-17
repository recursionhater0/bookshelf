from rest_framework import serializers

from authentication.serializers import CustomUserSerializer
from books.models import Book, BookPrice, BookCopy, Bookmark

from .generic import CreatedBySerializer


class BookListSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer()

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
        )


class BookCreateSerializer(CreatedBySerializer):

    class Meta:
        model = Book
        fields = (
            "title",
            "description",
            "is_active",
            "created_by"
        )
