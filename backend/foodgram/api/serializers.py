from reciepts.models import Ingredient, Tag
from rest_framework.serializers import ModelSerializer, ReadOnlyField, ManyRelatedField


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__', )


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__', )
