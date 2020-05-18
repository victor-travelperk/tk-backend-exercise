from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = ("name", "description", "ingredients")

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients", None)

        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)

        return recipe

    def update(self, instance, validated_data):
        """Update attributes for Recipe and remove old ingredients"""
        new_ingredients = validated_data.pop("ingredients", None)
        old_ingredients = Ingredient.objects.all().filter(recipe=instance)
        old_ingredients.delete()
        instance.name = validated_data["name"]
        instance.description = validated_data["description"]
        instance.save()

        for ingredient in new_ingredients:
            Ingredient.objects.create(recipe=instance, **ingredient)

        return instance
