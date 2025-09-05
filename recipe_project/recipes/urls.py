from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.recipe_list, name='recipe-list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='recipe-list'), name='logout'),
    path('register/', views.register, name='register'),
]
