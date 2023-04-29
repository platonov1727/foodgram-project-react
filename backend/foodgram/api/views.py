
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import (FavoriteRecipeSerializer,
                             IngredientSerializer,
                             RecipeCreateSerializer,
                             RecipeSerializer,
                             TagSerializer)

from reciepts.models import (Favorite,
                             Ingredient,
                             Recipe,
                             Tag,
                             Carts)


class TagAPIView(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientAPIView(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeAPIView(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer


class FavoriteRecipeView(APIView):
    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        favorite_recipe = Favorite(user=request.user, recipe=recipe)
        favorite_recipe.save()
        serializer = FavoriteRecipeSerializer(favorite_recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        try:
            favorite_recipe = get_object_or_404(Favorite,
                                                user=request.user,
                                                recipe=recipe)
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToCartView(APIView):
    def post(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            cart = Carts.objects.create(recipe=recipe, user=request.user)
            cart.save()
            return Response(status=status.HTTP_201_CREATED)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RemoveFromCartView(APIView):
    def delete(self, request, recipe_id):
        try:
            cart = Carts.objects.get(recipe_id=recipe_id, user=request.user)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Carts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DownloadShoppingCartView(APIView):
    def get(self, request):
        carts = Carts.objects.filter(user=request.user).all()
        ingredients_dict = {}
        for cart in carts:
            ingredients = cart.recipe.ingredients.all()
            for ingredient in ingredients:
                if ingredient.name in ingredients_dict:
                    ingredients_dict[ingredient.name] += ingredient.amount
                else:
                    ingredients_dict[ingredient.name] = ingredient.amount
        file_contents = ''
        for name, amount in ingredients_dict.items():
            file_contents += f'{name} - {amount}\n'
        response = HttpResponse(file_contents, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=shopping_cart.txt'
        return response
