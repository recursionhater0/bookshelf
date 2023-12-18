from django.urls import include, path
from rest_framework import routers

from .views import BookCopyViewSet, BookmarkViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register("bookmark", BookmarkViewSet)
router.register("review", ReviewViewSet)
router.register("", BookCopyViewSet)

urlpatterns = [path("", include(router.urls))]
