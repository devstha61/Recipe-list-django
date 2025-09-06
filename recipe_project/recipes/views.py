from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views


@login_required
def recipe_list(request):
    recipes = Recipe.objects.all()
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
