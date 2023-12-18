from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, decorators, permissions, viewsets, status
from rest_framework.response import Response

from books.filters import BookCopyFilter
from books.functions import remove_bookmark, add_to_bookmark
from books.models import BookCopy, Bookmark, Review
from books.serializers import BookCopySerializer, BookCopyDetailSerializer, BookmarkSerializer, ReviewCreateSerializer
from utils.mixins import MethodMatchingViewSetMixin


class BookCopyViewSet(MethodMatchingViewSetMixin, viewsets.ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer
    action_serializers = {
        "retrieve": BookCopyDetailSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ("get",)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("average_rating", "book__title",)
    ordering = ("book__title",)
    filterset_class = BookCopyFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ("list", "retrieve"):
            user = self.request.user
            bookmark_subquery = Bookmark.objects.filter(
                created_by=user,
                book_copy=models.OuterRef('pk')
            )
            return queryset.select_related("book").prefetch_related(
                "book__authors",
                "book__categories",
                "ratings",
            ).annotate(
                is_bookmarked=models.Exists(bookmark_subquery)
            )
        return queryset


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    http_method_names = ("post",)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add_to_bookmark(**serializer.validated_data)
        return Response({"message": "Book is successfully added to bookmark"}, status=status.HTTP_200_OK)

    @decorators.action(methods=["POST"], detail=False)
    def remove_bookmark(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        remove_bookmark(**serializer.validated_data)
        return Response({"message": "Book is successfully removed from bookmark"}, status=status.HTTP_200_OK)


class ReviewViewSet(MethodMatchingViewSetMixin, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    http_method_names = ("post",)
    permission_classes = (permissions.IsAuthenticated,)
