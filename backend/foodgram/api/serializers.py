import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from reciepts.models import (Favorite,
                             Ingredient,
                             IngredientRecipe,
                             Recipe,
                             Tag)
from users.serializers import UserRegistrationSerializer


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__', )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit')
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('amount', 'name', 'measurement_unit', 'id')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    author = UserRegistrationSerializer(
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user,
                                           recipe=obj).exists()
        return False

    def get_ingredients(self, obj):
        return IngredientRecipeSerializer(
            IngredientRecipe.objects.filter(recipe=obj).all(), many=True).data


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(child=serializers.DictField())
    author = UserRegistrationSerializer(
        default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    image = Base64ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tag_ids = validated_data.pop('tags', [])
        recipe = super().create(validated_data)
        for ingredient_data in ingredients_data:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_data['id'],
                amount=ingredient_data['amount']
            )
        recipe.tags.set(tag_ids)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tag_ids = validated_data.pop('tags', [])
        instance.image = validated_data.get('image', instance.image)
        IngredientRecipe.objects.filter(
            recipe=instance).delete()
        for ingredient_data in ingredients_data:
            IngredientRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient_data['id'],
                amount=ingredient_data['amount']
            )
        instance.tags.clear()
        instance.tags.set(tag_ids)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data

    def validate(self, data):
        name = data.get('name')
        cooking_time = data.get('cooking_time')
        amounts = data.get('ingredients')
        tags = data.get('tags')
        ingredients = data.get('ingredients')

        if len(name) < 1:
            raise serializers.ValidationError({
                'name': 'Название должно быть более 1 символа'})
        for ingredient in ingredients:
            if not Ingredient.objects.filter(
                    id=ingredient['id']).exists():
                raise serializers.ValidationError({
                    'ingredients': f'Ингредиента \
                    {ingredient["id"]} не существует'
                })
        if len(ingredients) != len(set([item['id'] for item in ingredients])):
            raise serializers.ValidationError(
                'Ингредиенты не могут повторяться, можете добавить количество')
        if len(tags) != len(set([item for item in tags])):
            raise serializers.ValidationError({
                'tags': 'Тэги не могут повторяться!'})
        if [item for item in amounts if item['amount'] < 1]:
            raise serializers.ValidationError({
                'amount': 'Количество должно быть более 0'
            })
        if cooking_time < 1:
            raise serializers.ValidationError({
                '''cooking_time': 'Время приготовления
                 не может быть мнее 1 минуты'''
            })
        return data

    class Meta:
        model = Recipe
        fields = '__all__'
