from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from reciepts.models import Ingredient

User = get_user_model()


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
