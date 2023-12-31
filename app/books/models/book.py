from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from utils.abstract import AbstractCreatedByModel, AbstractDateTimeModel

from ..translate import ftl_lazy
from .utils import get_book_cover_upload_path


class Book(AbstractDateTimeModel, AbstractCreatedByModel):
    title = models.CharField(
        max_length=255,
        verbose_name=ftl_lazy("book.title"),
    )
    description = models.TextField(verbose_name=ftl_lazy("book.description"))
    categories = models.ManyToManyField(
        to="books.Category", verbose_name=ftl_lazy("book.categories")
    )
    authors = models.ManyToManyField(
        to="books.Author", verbose_name=ftl_lazy("book.authors")
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
        verbose_name=ftl_lazy("book_copy.book"),
    )
    isbn = models.CharField(
        max_length=255, blank=True, verbose_name=ftl_lazy("book_copy.isbn")
    )
    publication_date = models.DateField(
        verbose_name=ftl_lazy("book_copy.publication_date")
    )
    publisher = models.ForeignKey(
        to="books.Publisher",
        on_delete=models.PROTECT,
        related_name="copies",
        verbose_name=ftl_lazy("book_copy.publisher"),
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name=ftl_lazy("book_copy.quantity")
    )
    cover_image = models.ImageField(
        upload_to=get_book_cover_upload_path,
        blank=True,
        verbose_name=ftl_lazy("book_copy.cover_image"),
    )

    def __str__(self):
        return f"{self.book.title}"

    class Meta:
        verbose_name = ftl_lazy("book_copy.verbose")
        verbose_name_plural = ftl_lazy("book_copy.plural")

    @property
    def average_rating(self):
        return self.ratings.aggregate(models.Avg("rating"))["rating__avg"]


class Category(AbstractDateTimeModel, AbstractCreatedByModel):
    name = models.CharField(max_length=255, verbose_name=ftl_lazy("category.name"))
    description = models.TextField(
        blank=True, verbose_name=ftl_lazy("category.description")
    )
    is_active = models.BooleanField(
        default=True, verbose_name=ftl_lazy("category.is_active")
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = ftl_lazy("category.verbose")
        verbose_name_plural = ftl_lazy("category.plural")


class Publisher(AbstractDateTimeModel, AbstractCreatedByModel):
    name = models.CharField(max_length=255, verbose_name=ftl_lazy("publisher.name"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = ftl_lazy("publisher.verbose")
        verbose_name_plural = ftl_lazy("publisher.plural")


class Review(AbstractCreatedByModel, AbstractDateTimeModel):
    rating = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=ftl_lazy("review.rating"),
    )
    book_copy = models.ForeignKey(
        to="books.BookCopy",
        on_delete=models.PROTECT,
        related_name="ratings",
        verbose_name=ftl_lazy("review.book_copy"),
    )
    comment = models.TextField(blank=True, verbose_name=ftl_lazy("review.comment"))

    def __str__(self):
        return f"{self.rating} {self.book_copy.book.title}"

    class Meta:
        verbose_name = ftl_lazy("review.verbose")
        verbose_name_plural = ftl_lazy("review.plural")


class Bookmark(AbstractDateTimeModel, AbstractCreatedByModel):
    book_copy = models.ForeignKey(
        to="books.BookCopy",
        on_delete=models.PROTECT,
        related_name="bookmarks",
        verbose_name=ftl_lazy("bookmark.book_copy"),
    )

    def __str__(self):
        return f"Bookmark {self.created_by.get_full_name()} {self.book_copy.book.title}"

    class Meta:
        verbose_name = ftl_lazy("bookmark.verbose")
        verbose_name_plural = ftl_lazy("bookmark.plural")
