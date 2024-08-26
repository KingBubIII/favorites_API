from django.shortcuts import render, HttpResponse, get_object_or_404, get_list_or_404
from .models import Favorites

def test(request):
    test = get_object_or_404(Favorites, id=0).name

    return HttpResponse(test)