from django.contrib.auth.models import User
from django.db import models


class Focus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Problem(models.Model):
    focus = models.ForeignKey(Focus, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_problems", blank=True)

    def __str__(self):
        return self.title


class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_solutions", blank=True)

    def __str__(self):
        return self.description


class Comment(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solution = models.ForeignKey(
        Solution, on_delete=models.CASCADE, null=True, blank=True
    )
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)

    def __str__(self):
        return self.text


class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    focus = models.ForeignKey(Focus, on_delete=models.CASCADE, related_name="followers")
