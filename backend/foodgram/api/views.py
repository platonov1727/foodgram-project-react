from api.serializers import TagSerializer, IngredientSerializer
from reciepts.models import Tag, Ingredient
from rest_framework.viewsets import ViewSet


class TagAPIView(ViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientAPIView(ViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
