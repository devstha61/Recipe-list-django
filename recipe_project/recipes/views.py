from django.shortcuts import render
from .models import Recipe

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, "../templates/recipe_list.html", {'recipes': recipes})

