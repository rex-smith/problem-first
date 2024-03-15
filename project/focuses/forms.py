# forms.py
from django import forms

from .models import Focus, Item

from .models import Focus, Item


class FocusForm(forms.ModelForm):
    class Meta:
        model = Focus
        fields = ["name", "description"]


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "focus"]


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["description", "problem"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["text", "problem", "solution", "parent_comment"]
