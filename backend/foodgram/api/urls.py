from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteRecipeViewSet,
                       IngredientAPIView,
                       RecipeAPIView,
                       ShoppingCartViewSet,
                       TagAPIView)

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientAPIView)
router_v1.register(r'tags', TagAPIView)
router_v1.register(r'recipes', RecipeAPIView)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteRecipeViewSet,
    basename='favorite')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet,
    basename='shoppingcart')


urlpatterns = [
    path('', include(router_v1.urls)),
]
