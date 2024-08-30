from django.shortcuts import HttpResponse, get_object_or_404, get_list_or_404
from .models import Favorites
from django.http import JsonResponse


def top_in_category(request, amount, category):
    top_favorites = get_list_or_404(
        Favorites.objects.defer("category")
        .filter(category__iexact=category)
        .filter(rank__lte=amount)
        .order_by("rank")
        .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
    )

    return JsonResponse(top_favorites, safe=False)


def top_all(request, amount):
    all_categories = list(
        Favorites.objects.values_list("category", flat=True).distinct()
    )
    print(all_categories)

    top_favorites = {}
    for curr_category in all_categories:
        top_in_category = get_list_or_404(
            Favorites.objects.defer("category")
            .filter(category__iexact=curr_category)
            .filter(rank__lte=amount)
            .order_by("rank")
            .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
        )

        top_favorites[curr_category] = top_in_category

    return JsonResponse(top_favorites)
