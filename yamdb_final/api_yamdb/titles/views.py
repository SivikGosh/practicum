from api.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, pagination, viewsets

from . import models, serializers
from .filters import TitleFilter


class BaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет с нужными миксинами для наследования."""
    pass


class CategoryViewSet(BaseViewSet):
    """Вьюсет категорий."""

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    filterset_fields = ('slug',)
    lookup_field = 'slug'


class GenreViewSet(BaseViewSet):
    """Вьюсет жанров."""

    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    filterset_fields = ('slug',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""

    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    filterset_class = TitleFilter
