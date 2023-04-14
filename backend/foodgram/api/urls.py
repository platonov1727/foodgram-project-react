from django.urls import path, include, re_path
from api.views import TagAPIView, IngredientAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ingredients', IngredientAPIView)
router.register(r'tag', TagAPIView)


urlpatterns = [
    path(r'', include('djoser.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken')),
    path('ingredients/', include(router.urls)),
]
