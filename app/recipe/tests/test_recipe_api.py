from unittest import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from core.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def get_recipe_detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_sample_recipe(name='Krusty krab burguer', description='Best in bikini botton'):
    return Recipe.objects.create(
        name=name,
        description=description
    )


def create_sample_ingredient(recipe, name='Tomato'):
    return Ingredient.objects.create(
        name=name,
        recipe=recipe
    )


class TestRecipeApi(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_recipes(self):
        recipe_with_ingredients = create_sample_recipe()
        recipe_with_ingredients.ingredients.add(
            create_sample_ingredient(recipe_with_ingredients)
        )
        create_sample_recipe()

        res = self.client.get(RECIPES_URL)
        
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        recipe_with_ingredients = create_sample_recipe()
        recipe_with_ingredients.ingredients.add(
            create_sample_ingredient(recipe_with_ingredients)
        )

        url = get_recipe_detail_url(recipe_with_ingredients.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe_with_ingredients)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)