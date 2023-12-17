from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from books.serializers import BookCreateSerializer, BookListSerializer
from utils.mixins import MethodMatchingViewSetMixin


class BookViewSet(MethodMatchingViewSetMixin, ModelViewSet):
    queryset = Book.objects.all()

    serializer_class = BookListSerializer
    action_serializers = {
        "create": BookCreateSerializer,
        "list": BookListSerializer,
    }

    permission_classes = (permissions.IsAuthenticated,)
