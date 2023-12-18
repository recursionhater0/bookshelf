from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError

from .models import BookCopy, Bookmark

User = get_user_model()


def add_to_bookmark(book_copy: BookCopy, created_by: User):
    if Bookmark.objects.filter(created_by=created_by, book_copy=book_copy).exists():
        raise ValidationError("This book is already in bookmarks")

    Bookmark.objects.create(book_copy=book_copy, created_by=created_by)


def remove_bookmark(book_copy: BookCopy, created_by: User):
    Bookmark.objects.filter(created_by=created_by, book_copy=book_copy).delete()
