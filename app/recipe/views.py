from rest_framework.viewsets import ModelViewSet

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all().order_by("-id")

    def get_queryset(self):
        queryset = Recipe.objects.all()
        name_filter = self.request.query_params.get("name", None)
        if name_filter:
            queryset = queryset.filter(name__contains=name_filter)
        return queryset.order_by("-id")

