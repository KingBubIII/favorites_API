from django.shortcuts import HttpResponse, get_object_or_404, get_list_or_404
from .models import Favorites
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Subquery
from random import choice


# Gets top X rated items in a category. Category and X defined by user in url
# Returns list in JSON format
def top_in_category(request, amount, category):
    # Filters all favorite items based on rank and category
    top_favorites = get_list_or_404(
        Favorites.objects.filter(category__iexact=category)
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
            Favorites.objects.filter(category__iexact=curr_category)
            .filter(rank__lte=amount)
            .order_by("rank")
            .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
        )

    return JsonResponse(top_favorites)


def latest(request):
    subquery_timestamp = Favorites.objects.order_by("-date_added").values("date_added")[
        :1
    ]

    most_recent_favorites = get_list_or_404(
        Favorites.objects.filter(date_added__exact=Subquery(subquery_timestamp)).values(
            "id", "name", "rank", "comments", "link", "added_by_suggestion", "category"
        )
    )

    return JsonResponse(most_recent_favorites, safe=False)


def latest_by_category(request, category):
    subquery_timestamp = Favorites.objects.order_by("-date_added").values("date_added")[
        :1
    ]

    most_recent_favorites = get_list_or_404(
        Favorites.objects.filter(category__iexact=category)
        .filter(date_added__exact=Subquery(subquery_timestamp))
        .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
    )

    return JsonResponse(most_recent_favorites, safe=False)


def random_favorite(request):
    # gets all ids from favorites table without loading other fields
    pks = Favorites.objects.values_list("pk", flat=True)
    # picks a random id
    random_pk = choice(pks)
    # filters to only the chosen id and puts in a list to get values easier
    random_obj = get_list_or_404(
        Favorites.objects.filter(pk=random_pk).values(
            "id", "name", "rank", "comments", "link", "added_by_suggestion"
        )
    )[0]

    return JsonResponse(random_obj)


def random_favorite_in_category(request, category):
    # gets all ids from category without loading other fields
    pks = Favorites.objects.filter(category__iexact=category).values_list(
        "pk", flat=True
    )
    # picks a random id
    random_pk = choice(pks)
    # filters to only the chosen id and puts in a list to get values easier
    random_obj = get_list_or_404(
        Favorites.objects.filter(pk=random_pk).values(
            "id", "name", "rank", "comments", "link", "added_by_suggestion"
        )
    )[0]

    return JsonResponse(random_obj)
