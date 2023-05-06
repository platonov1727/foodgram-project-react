from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from reciepts.models import (FavoriteRecipe,
                             Ingredient,
                             IngredientRecipe,
                             Recipe,
                             Tag)


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
    list_display = ('name', 'measurement_unit', 'id')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TagsResource(resources.ModelResource):
    name = Field(
        column_name='name', attribute='name',)
    color = Field(
        column_name='color', attribute='color',)
    slug = Field(attribute='slug', column_name='slug')
    id = Field(attribute='id', column_name='id')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    resource_class = TagsResource
    list_display = ('name', 'color', 'slug', 'id')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'recipe', 'amount']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'cooking_time',
                    'pub_date', 'author', 'id']


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_recipe']
