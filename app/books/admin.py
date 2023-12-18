from django.contrib import admin
from django.http.request import HttpRequest

from .models import *


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "middle_name",
    )
    search_fields = ("first_name", "last_name", "middle_name")
    autocomplete_fields = ("created_by",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rating",
        "comment",
        "get_book_name",
    )
    autocomplete_fields = ("created_by",)

    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        return qs.select_related("book_copy__book")

    @admin.display(description="book name")
    def get_book_name(self, obj: Review):
        return obj.book_copy.book.title


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    autocomplete_fields = ("created_by",)


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "isbn",
        "publication_date",
        "quantity",
        "created_by",
        "get_book_name",
    )
    autocomplete_fields = ("created_by", "book", "publisher")
    list_select_related = ("created_by", "book")
    inlines = (ReviewInline,)

    @admin.display(description="book name")
    def get_book_name(self, obj: BookCopy):
        return obj.book.title


@admin.register(BookPrice)
class BookPriceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "price",
        "get_book_name",
        "created_by",
    )
    list_select_related = ("book", "created_by")
    autocomplete_fields = ("created_by", "book")

    @admin.display(description="book name")
    def get_book_name(self, obj: BookPrice):
        return obj.book.title


class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 1
    autocomplete_fields = ("created_by", "publisher")


class BookPriceInline(admin.TabularInline):
    model = BookPrice
    extra = 1
    autocomplete_fields = ("created_by",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "get_short_description",
        "created_at",
        "updated_at",
        "created_by",
    )
    list_select_related = ("created_by",)
    autocomplete_fields = ("created_by", "categories", "authors")
    search_fields = (
        "title",
        "authors__first_name",
        "authors__last_name",
        "authors__middle_name",
    )
    inlines = (BookCopyInline, BookPriceInline)

    @admin.display(description="short description")
    def get_short_description(self, obj: Book):
        return obj.description[:20]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "get_short_description",
        "is_active",
        "created_by",
    )
    search_fields = ("name",)
    autocomplete_fields = ("created_by",)

    @admin.display(description="short description")
    def get_short_description(self, obj: Category):
        return obj.description[:10]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    autocomplete_fields = ("created_by",)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_book_name",
        "created_by",
    )
    list_select_related = ("created_by", "book_copy")

    @admin.display(description="short description")
    def get_book_name(self, obj: Bookmark):
        return obj.book_copy.book.title
