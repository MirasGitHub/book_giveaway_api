import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    author__name__icontains = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    genre__name__icontains = django_filters.CharFilter(field_name='genre__name', lookup_expr='icontains')
    condition__icontains = django_filters.CharFilter(field_name='condition', lookup_expr='icontains')
    title__icontains = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    location__icontains = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    owner = django_filters.NumberFilter(field_name='owner__id')
    is_available = django_filters.BooleanFilter(field_name='is_available', widget=django_filters.widgets.BooleanWidget())

    class Meta:
        model = Book
        fields = ['author__name__icontains', 'genre__name__icontains', 'condition__icontains', 'title__icontains', 'location__icontains', 'owner', 'is_available']
