from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from utils.abstract import AbstractDateTimeModel, AbstractCreatedByModel

from .utils import get_book_cover_upload_path


class Book(AbstractDateTimeModel, AbstractCreatedByModel):
    title = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    categories = models.ManyToManyField(
        to="books.Category",
    )
    authors = models.ManyToManyField(
        to="books.Author",
    )

    def __str__(self):
        return f"{self.title}"


class BookCopy(AbstractCreatedByModel, AbstractDateTimeModel):
    book = models.ForeignKey(
        to="books.Book",
        on_delete=models.PROTECT,
        related_name="book_copies",
    )
    isbn = models.CharField(
        max_length=255,
        blank=True,
    )
    publication_date = models.DateField()
    publisher = models.ForeignKey(
        to="books.Publisher",
        on_delete=models.PROTECT,
        related_name="copies",
    )
    quantity = models.PositiveBigIntegerField()
    cover_image = models.ImageField(upload_to=get_book_cover_upload_path, blank=True)

    def __str__(self):
        return f"{self.book.title}"

    @property
    def average_rating(self):
        return self.ratings.aggregate(models.Avg('rating'))['rating__avg']


class Category(AbstractDateTimeModel, AbstractCreatedByModel):
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,
    )
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.name}"


class Publisher(AbstractDateTimeModel, AbstractCreatedByModel):
    name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return f"{self.name}"


class Review(AbstractCreatedByModel, AbstractDateTimeModel):
    rating = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
    )
    book_copy = models.ForeignKey(
        to="books.BookCopy",
        on_delete=models.PROTECT,
        related_name="ratings",
    )
    comment = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.rating} {self.book_copy.book.title}"


class Bookmark(AbstractDateTimeModel, AbstractCreatedByModel):
    book_copy = models.ForeignKey(
        to="books.BookCopy",
        on_delete=models.PROTECT,
        related_name="bookmarks",
    )

    def __str__(self):
        return f"Bookmark {self.created_by.get_full_name()} {self.book_copy.book.title}"
