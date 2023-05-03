from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientAPIView,
                       RecipeAPIView,
                       TagAPIView,
                       FavoriteRecipeViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientAPIView)
router_v1.register(r'tags', TagAPIView)
router_v1.register(r'recipes', RecipeAPIView)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteRecipeViewSet,
    basename='favorite')

urlpatterns = [
    path(r'', include('djoser.urls')),
    path('', include(router_v1.urls)),
]
