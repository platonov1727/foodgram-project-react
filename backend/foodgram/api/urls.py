from django.urls import path, include, re_path
from api.views import TagAPIView, IngredientAPIView, RecipeAPIView, FavoriteRecipeView
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
]
