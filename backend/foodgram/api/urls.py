from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AddToCartView,
                       DownloadShoppingCartView,
                       FavoriteRecipeView,
                       IngredientAPIView,
                       RecipeAPIView,
                       RemoveFromCartView,
                       TagAPIView)

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientAPIView)
router_v1.register(r'tags', TagAPIView)
router_v1.register(r'recipes', RecipeAPIView)

urlpatterns = [
    path(r'', include('djoser.urls')),
    path('', include(router_v1.urls)),
    path('recipes/<int:recipe_id>/favorite', FavoriteRecipeView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', AddToCartView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/',
         RemoveFromCartView.as_view()),
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartView.as_view()),
]
