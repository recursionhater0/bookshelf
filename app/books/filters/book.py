from django_filters import rest_framework as filters

from books.models import Author, BookCopy, Category


class BookCopyFilter(filters.FilterSet):
    categories = filters.ModelMultipleChoiceFilter(
        field_name="book__categories",
        to_field_name="id",
        queryset=Category.objects.all(),
        conjoined=True,
    )
    authors = filters.ModelMultipleChoiceFilter(
        field_name="book__authors",
        to_field_name="id",
        queryset=Author.objects.all(),
        conjoined=True,
    )
    publication_date = filters.DateFromToRangeFilter()

    class Meta:
        model = BookCopy
        fields = (
            "categories",
            "publication_date",
        )
