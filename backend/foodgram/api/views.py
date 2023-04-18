from api.serializers import TagSerializer, IngredientSerializer
from reciepts.models import Tag, Ingredient
from rest_framework.viewsets import ModelViewSet


class TagAPIView(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientAPIView(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
