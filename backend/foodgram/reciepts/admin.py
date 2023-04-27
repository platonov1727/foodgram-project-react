from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from reciepts.models import (Carts, Favorite, Ingredient, IngredientRecipe,
                             Recipe, Tag)


class IngredientsResource(resources.ModelResource):
    name = Field(
        column_name='name', attribute='name',)
    measurement_unit = Field(
        column_name='measurement_unit', attribute='measurement_unit',)
    id = Field(attribute='id', column_name='id')

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientsResource
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Tag)
admin.site.register(IngredientRecipe)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(Carts)
