from unittest import TestCase
from core.models import Recipe, Ingredient


class TestModels(TestCase):
    """Tests for model basic behavior"""

    def test_recipe_str(self):
        recipe = Recipe.objects.create(
            name="Pita Kebab",
            description="Classic chicken Kebab with everything included",
        )
        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        recipe = Recipe.objects.create(
            name="Pepperoni Pizza", description="Single ingredient pizza, best in town"
        )
        ingredient = Ingredient.objects.create(name="Pepperoni", recipe=recipe)
        self.assertEqual(str(ingredient), ingredient.name)
