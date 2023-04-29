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
        default=serializers.CurrentUserDefault())
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='name',
        many=True
    )
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user,
                                           recipe=obj).exists()
        return False

    class Meta:
        model = Recipe
        fields = '__all__'

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

    def to_representation(self, obj):
        self.fields.pop('ingredients')
        representation = super().to_representation(obj)
        representation['ingredients'] = IngredientRecipeSerializer(
            IngredientRecipe.objects.filter(recipe=obj).all(), many=True).data
        return representation

    class Meta:
        model = Recipe
        fields = '__all__'
