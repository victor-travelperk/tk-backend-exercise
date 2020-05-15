from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'ingredients')

    def create(self, validated_data):
        ingredients = None
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients', None)

        recipe = Recipe.objects.create(**validated_data)

        if ingredients:
            for ingredient in ingredients:
                Ingredient.objects.create(recipe=recipe, **ingredient)

        return recipe
