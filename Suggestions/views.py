from django.shortcuts import HttpResponse, get_object_or_404, get_list_or_404
from .models import Suggestions
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Subquery
from random import choice


# Gets top X rated items in a category. Category and X defined by user in url
# Returns list in JSON format
def top_in_category(request, amount, category):
    if request.method == "GET":
        # Filters all favorite items based on rank and category
        top_favorites = get_list_or_404(
            Suggestions.objects.filter(category__iexact=category)
            .filter(rank__lte=amount)
            .order_by("rank")
            .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
        )

        return JsonResponse(top_favorites, safe=False)


# Gets top X rated items in every category
# Returns dictionary in JSON format
def top_all(request, amount):
    if request.method == "GET":
        # Gets all categories from database
        all_categories = list(
            Suggestions.objects.values_list("category", flat=True).distinct()
        )
        print(all_categories)

        # Dictionary to be retuned
        top_favorites = {}
        for curr_category in all_categories:
            # Filters all favorite items based on rank and category
            top_favorites[curr_category] = get_list_or_404(
                Suggestions.objects.filter(category__iexact=curr_category)
                .filter(rank__lte=amount)
                .order_by("rank")
                .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
            )

        return JsonResponse(top_favorites)


def latest(request):
    if request.method == "GET":
        subquery_timestamp = Suggestions.objects.order_by("-date_added").values(
            "date_added"
        )[:1]

        most_recent_favorites = get_list_or_404(
            Suggestions.objects.filter(
                date_added__exact=Subquery(subquery_timestamp)
            ).values(
                "id",
                "name",
                "rank",
                "comments",
                "link",
                "added_by_suggestion",
                "category",
            )
        )

        return JsonResponse(most_recent_favorites, safe=False)


def latest_by_category(request, category):
    if request.method == "GET":
        subquery_timestamp = Suggestions.objects.order_by("-date_added").values(
            "date_added"
        )[:1]

        most_recent_favorites = get_list_or_404(
            Suggestions.objects.filter(category__iexact=category)
            .filter(date_added__exact=Subquery(subquery_timestamp))
            .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
        )

        return JsonResponse(most_recent_favorites, safe=False)


def random_favorite(request):
    if request.method == "GET":
        # gets all ids from Suggestions table without loading other fields
        pks = Suggestions.objects.values_list("pk", flat=True)
        # picks a random id
        random_pk = choice(pks)
        # filters to only the chosen id and puts in a list to get values easier
        random_obj = get_list_or_404(
            Suggestions.objects.filter(pk=random_pk).values(
                "id", "name", "rank", "comments", "link", "added_by_suggestion"
            )
        )[0]

        return JsonResponse(random_obj)


def random_favorite_in_category(request, category):
    if request.method == "GET":
        # gets all ids from category without loading other fields
        pks = Suggestions.objects.filter(category__iexact=category).values_list(
            "pk", flat=True
        )
        # picks a random id
        random_pk = choice(pks)
        # filters to only the chosen id and puts in a list to get values easier
        random_obj = get_list_or_404(
            Suggestions.objects.filter(pk=random_pk).values(
                "id", "name", "rank", "comments", "link", "added_by_suggestion"
            )
        )[0]

        return JsonResponse(random_obj)


def search_favorites(request, str_match):
    if request.method == "GET":
        # searches database name column
        results = get_list_or_404(
            Suggestions.objects.filter(name__icontains=str_match).values(
                "id", "name", "rank", "comments", "link", "added_by_suggestion"
            )
        )

        return JsonResponse(results, safe=False)


def search_favorites_in_category(request, str_match, category):
    if request.method == "GET":
        # filters to category first then searches database name column
        results = get_list_or_404(
            Suggestions.objects.filter(category__iexact=category)
            .filter(name__icontains=str_match)
            .values("id", "name", "rank", "comments", "link", "added_by_suggestion")
        )

        return JsonResponse(results, safe=False)
