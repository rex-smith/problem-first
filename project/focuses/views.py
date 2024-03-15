from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Comment, Focus, Problem, Solution, UserFollows


def index(request):
    focuses = Focus.objects.all()
    return render(request, "focuses/index.html", {"focuses": focuses})


def detail(request, focus_name):
    focus = Focus.objects.get(name=focus_name)
    problems = (
        Problem.objects.filter(focus=focus)
        .prefetch_related(
            Prefetch(
                "solution_set",
                queryset=Solution.objects.order_by("-created_at").prefetch_related(
                    "likes"
                ),
            ),
            Prefetch(
                "comment_set",
                queryset=Comment.objects.order_by("-created_at").prefetch_related(
                    "likes"
                ),
            ),
        )
        .order_by("-created_at")
    )
    return render(
        request, "focuses/detail.html", {"focus": focus, "problems": problems}
    )


@login_required
def follow_focus(request, focus_id):
    focus = Focus.objects.get(id=focus_id)
    UserFollows.objects.create(user=request.user, focus=focus)
    return redirect("feed")


@login_required
def unfollow_focus(request, focus_id):
    focus = Focus.objects.get(id=focus_id)
    UserFollows.objects.filter(user=request.user, focus=focus).delete()
    return redirect("feed")


def feed(request):
    followed_focuses = request.user.userfollows_set.values_list("focus_id", flat=True)
    if followed_focuses:
        problems = Problem.objects.filter(focus__in=followed_focuses)
    else:
        problems = Problem.objects.all().select_related("focus")
    problem_ids = [problem.id for problem in problems]
    problem_queryset = Problem.objects.filter(id__in=problem_ids)

    problems_with_related = problem_queryset.prefetch_related(
        Prefetch(
            "solution_set",
            queryset=Solution.objects.order_by("-created_at").prefetch_related("likes"),
        ),
        Prefetch(
            "comment_set",
            queryset=Comment.objects.order_by("-created_at").prefetch_related("likes"),
        ),
    ).order_by("-created_at")
    return render(request, "feed.html", {"problems": problems_with_related})
