from rest_framework.viewsets import ModelViewSet

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all().order_by('-id')
