from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('recipe-list')
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})