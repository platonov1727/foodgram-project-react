from api.views import (AddToCartView, DownloadShoppingCartView,
                       FavoriteRecipeView, IngredientAPIView, RecipeAPIView,
                       RemoveFromCartView, TagAPIView)
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ingredients', IngredientAPIView)
router.register(r'tags', TagAPIView)
router.register(r'recipes', RecipeAPIView)

urlpatterns = [
    path(r'', include('djoser.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/favorite', FavoriteRecipeView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', AddToCartView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', RemoveFromCartView.as_view()),
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartView.as_view()),
]
