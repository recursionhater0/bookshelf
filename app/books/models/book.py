from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from utils.abstract import AbstractDateTimeModel, AbstractCreatedByModel

from .utils import get_book_cover_upload_path
from ..translate import ftl_lazy


class Book(AbstractDateTimeModel, AbstractCreatedByModel):
    title = models.CharField(
        max_length=255,
        verbose_name=ftl_lazy("book.title"),
    )
    description = models.TextField(
        verbose_name=ftl_lazy("book.description")
    )
    categories = models.ManyToManyField(
        to="books.Category",
        verbose_name=ftl_lazy("book.categories")
    )
    authors = models.ManyToManyField(
        to="books.Author",
        verbose_name=ftl_lazy("book.authors")
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = ftl_lazy("book.verbose")
        verbose_name_plural = ftl_lazy("book.plural")


class BookCopy(AbstractCreatedByModel, AbstractDateTimeModel):
    book = models.ForeignKey(
        to="books.Book",
        on_delete=models.PROTECT,
        related_name="book_copies",
        verbose_name=ftl_lazy("book_copy.book")
    )
    isbn = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=ftl_lazy("book_copy.isbn")
    )
    publication_date = models.DateField(
        verbose_name=ftl_lazy("book_copy.publication_date")
    )
    publisher = models.ForeignKey(
        to="books.Publisher",
        on_delete=models.PROTECT,
        related_name="copies",
        verbose_name=ftl_lazy("book_copy.publisher")
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name=ftl_lazy("book_copy.quantity")
    )
    cover_image = models.ImageField(
        upload_to=get_book_cover_upload_path,
        blank=True,
        verbose_name=ftl_lazy("book_copy.cover_image")
    )

    def __str__(self):
        return f"{self.book.title}"

    class Meta:
        verbose_name = ftl_lazy("book_copy.verbose")
        verbose_name_plural = ftl_lazy("book_copy.plural")

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
