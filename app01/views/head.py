from django.shortcuts import render


def head(request):
    return render(request, "head.html")
