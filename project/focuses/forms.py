# forms.py
from django import forms

from .models import Comment, Focus, Problem, Solution


class FocusForm(forms.ModelForm):
    class Meta:
        model = Focus
        fields = ["name"]


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ["title", "description"]


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ["description"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
