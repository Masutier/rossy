from django.contrib import messages
from django.shortcuts import render, redirect


def home (request):

    context={"title": "Home"}
    return render(request, 'rossy/home.html', context)
