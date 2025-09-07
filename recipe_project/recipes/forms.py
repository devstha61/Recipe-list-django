from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    publish = forms.BooleanField(required=False, initial=False, label="Publish now")

    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'image']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 6}),
        }
