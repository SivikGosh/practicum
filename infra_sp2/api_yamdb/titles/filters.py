import django_filters

from .models import Title


class TitleFilter(django_filters.FilterSet):
    """Фильтрация произведений по названию, году, жанру, категориям."""
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact'
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.CharFilter(
        field_name='year',
        lookup_expr='iexact'
    )

    class Meta:
        model = Title
        fields = '__all__'
