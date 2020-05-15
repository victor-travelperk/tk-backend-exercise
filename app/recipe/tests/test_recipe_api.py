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

    def test_list_recipes_with_filter(self):
        recipe1 = create_sample_recipe(
            name='Big Mac'
        )

        create_sample_recipe(name='Whopper')

        res = self.client.get(RECIPES_URL, {'name': 'Big'})

        serializer = RecipeSerializer(recipe1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(serializer.data, res.data[0])

    def test_create_recipe_successful(self):
        payload = {
            'name': 'Mysterious Chicken nuggets',
            'description': 'N',
            'ingredients': [
                {'name': 'Natural additives'},
                {'name': 'Maybe soylent green'},
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        new_recipe = Recipe.objects.all().filter(name=payload['name'])[0]
        new_recipe_serialized = RecipeSerializer(new_recipe)
        self.assertEqual(
            len(new_recipe_serialized.data['ingredients']),
            2
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_recipe_invalid(self):
        payload = {'name': ''}

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_recipe_successful(self):
        recipe = create_sample_recipe(
            name='Burrito light',
            description='Burrito for a quick bite'
        )
        create_sample_ingredient(recipe, name='Wrap')
        create_sample_ingredient(recipe, name='Cochinillo')

        payload = {
            'name': 'Ultra burrito',
            'description': 'Best way to welcome your cheat day',
            'ingredients': [
                {'name': 'Extra thick flour tortilla'},
                {'name': 'Salsa la vista'}
            ]
        }

        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()

        self.assertEqual(payload['name'], recipe.name)
        self.assertEqual(payload['description'], recipe.description)

        # Validate that the only new ingredients are present
        ingredients = recipe.ingredients.all().order_by('name')
        payload_ingredients = sorted(payload['ingredients'], key=lambda x: x['name'])
        self.assertEqual(len(ingredients), 2)
        self.assertEqual(payload_ingredients[0]['name'], ingredients[0].name)
        self.assertEqual(payload_ingredients[1]['name'], ingredients[1].name)
