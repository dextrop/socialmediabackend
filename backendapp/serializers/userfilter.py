# filters.py
import django_filters
from backendapp.models import Users


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        name = "users"
        model = Users
        fields = ['username', 'email', 'name']
