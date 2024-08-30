from django.shortcuts import HttpResponse, get_object_or_404, get_list_or_404
from .models import Favorites
from django.http import JsonResponse


# Gets top X rated items in a category. Category and X defined by user in url
# Returns list in JSON format
def top_in_category(request, amount, category):
    # Filters all favorite items based on rank and category
    top_favorites = get_list_or_404(
        Favorites.objects.defer("category")
        .filter(category__iexact=category)
        .filter(rank__lte=amount)
        .order_by("rank")
        .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
    )

    return JsonResponse(top_favorites, safe=False)


# Gets top X rated items in every category
# Returns dictionary in JSON format
def top_all(request, amount):
    # Gets all categories from database
    all_categories = list(
        Favorites.objects.values_list("category", flat=True).distinct()
    )
    print(all_categories)

    # Dictionary to be retuned
    top_favorites = {}
    for curr_category in all_categories:
        # Filters all favorite items based on rank and category
        top_favorites[curr_category] = get_list_or_404(
            Favorites.objects.defer("category")
            .filter(category__iexact=curr_category)
            .filter(rank__lte=amount)
            .order_by("rank")
            .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
        )

    return JsonResponse(top_favorites)
