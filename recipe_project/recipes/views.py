from django.shortcuts import render
from recipe_project.recipes.models import Recipe

# Create your views here.
def recipe_list(request):
    recipes = Recipe.objects.all()
    return(render,
           "recipe_list.html",
           {recipes: recipes})