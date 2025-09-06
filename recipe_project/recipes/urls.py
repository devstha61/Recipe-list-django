from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.recipe_list, name='recipe-list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe-detail'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
]
