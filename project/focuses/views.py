from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import CommentForm, FocusForm, ProblemForm, SolutionForm
from .models import Comment, Focus, Problem, Solution, UserFollows


def index(request):
    focuses = Focus.objects.all()
    # Include focus form
    if request.method == "POST":
        form = FocusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = FocusForm()

    return render(request, "focuses/index.html", {"focuses": focuses, "form": form})


def detail(request, focus_slug):
    focus = Focus.objects.get(slug=focus_slug)
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
    if request.method == "POST":
        problem_form = ProblemForm(request.POST)
        if problem_form.is_valid():
            problem = problem_form.save(commit=False)
            problem.focus = focus
            problem.created_by = request.user
            problem.save()
            return redirect("focuses:detail", focus_slug=focus.slug)
    else:
        problem_form = ProblemForm()

    return render(
        request,
        "focuses/detail.html",
        {
            "focus": focus,
            "problems": problems,
            "problem_form": problem_form,
        },
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
    # Include problem creation form
    problem_form = ProblemForm()
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
    return render(
        request,
        "feed.html",
        {"problems": problems_with_related, "problem_form": problem_form},
    )
