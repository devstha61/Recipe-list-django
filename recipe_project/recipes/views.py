from django.http import HttpResponseForbidden
from django.utils import timezone 
from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import RecipeForm


@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(published_at__isnull=False)
    return render(request, 'recipe_list.html', {'recipes': recipes})


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def register(request):
    if request.user.is_authenticated:
        return redirect('recipe-list')  # Redirect if already logged in

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('recipe-list')
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})



class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('recipe-list')
        return super().dispatch(request, *args, **kwargs)

@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            # Handle publish checkbox
            if form.cleaned_data.get("publish"):
                recipe.published_at = timezone.now()
            else:
                recipe.published_at = None
            recipe.save()
            return redirect("recipe-detail", pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, "recipe_form.html", {"form": form, "create": True})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Only allow author to edit
    if request.user != recipe.author:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            # Handle publish checkbox
            if form.cleaned_data.get("publish"):
                recipe.published_at = timezone.now()
            else:
                recipe.published_at = None
            recipe.save()
            return redirect("recipe-detail", pk=recipe.pk)
    else:
        # Pre-fill the publish checkbox based on current status
        initial_data = {"publish": recipe.published_at is not None}
        form = RecipeForm(instance=recipe, initial=initial_data)

    return render(request, "recipe_form.html", {"form": form, "create": False})

def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Only allow author to delete
    if request.user != recipe.author:
        return HttpResponseForbidden("You are not allowed to delete this recipe.")

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe-list')

    return render(request, 'recipe_confirm_delete.html', {'recipe': recipe})

@login_required
def my_recipes(request):
    user = request.user
    published_recipes = Recipe.objects.filter(author=user, published_at__isnull=False)
    unpublished_recipes = Recipe.objects.filter(author=user, published_at__isnull=True)

    context = {
        'published_recipes': published_recipes,
        'unpublished_recipes': unpublished_recipes,
    }
    return render(request, 'my_recipes.html', context)