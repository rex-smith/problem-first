from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the focuses index.")


def detail(request, focus_id):
    return HttpResponse("You're looking at focus %s." % focus_id)
