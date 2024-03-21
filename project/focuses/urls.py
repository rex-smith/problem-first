from django.urls import path

from . import views

app_name = "focuses"
urlpatterns = [
    path("", views.index, name="index"),
    path("feed/", views.feed, name="feed"),
    path("<slug:focus_slug>/", views.detail, name="detail"),
    path("follow/<int:focus_id>/", views.follow_focus, name="follow_focus"),
    path("unfollow/<int:focus_id>/", views.unfollow_focus, name="unfollow_focus"),
]
