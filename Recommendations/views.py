from django.shortcuts import HttpResponse, get_object_or_404, get_list_or_404
from .models import Recommendations
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Subquery
from random import choice


# this is for the values method instead of hard-coding each attribute I need usually
def _std_attributes(category=True):
    attributes = ["id", "name", "comments", "link", "suggester"]
    if category:
        attributes.append("category")

    return attributes


def latest(request):
    if request.method == "GET":
        subquery_timestamp = Recommendations.objects.order_by("-date_added").values(
            "date_added"
        )[:1]

        most_recent_favorites = get_list_or_404(
            Recommendations.objects.filter(
                date_added__exact=Subquery(subquery_timestamp)
            ).values(*_std_attributes())
        )

        return JsonResponse(most_recent_favorites, safe=False)


def latest_by_category(request, category):
    if request.method == "GET":
        subquery_timestamp = Recommendations.objects.order_by("-date_added").values(
            "date_added"
        )[:1]

        most_recent_favorites = get_list_or_404(
            Recommendations.objects.filter(category__iexact=category)
            .filter(date_added__exact=Subquery(subquery_timestamp))
            .values(*_std_attributes(False))
        )

        return JsonResponse(most_recent_favorites, safe=False)


def random_recommendation(request):
    if request.method == "GET":
        # gets all ids from Recommendations table without loading other fields
        pks = Recommendations.objects.values_list("pk", flat=True)
        # picks a random id
        random_pk = choice(pks)
        # filters to only the chosen id and puts in a list to get values easier
        random_obj = get_list_or_404(
            Recommendations.objects.filter(pk=random_pk).values(*_std_attributes())
        )[0]

        return JsonResponse(random_obj)


def random_recommendation_from_category(request, category):
    if request.method == "GET":
        # gets all ids from category without loading other fields
        pks = Recommendations.objects.filter(category__iexact=category).values_list(
            "pk", flat=True
        )
        # picks a random id
        random_pk = choice(pks)
        # filters to only the chosen id and puts in a list to get values easier
        random_obj = get_list_or_404(
            Recommendations.objects.filter(pk=random_pk).values(*_std_attributes(False))
        )[0]

        return JsonResponse(random_obj)


def search_recommendation(request, str_match):
    if request.method == "GET":
        # searches database name column
        results = get_list_or_404(
            Recommendations.objects.filter(name__icontains=str_match).values(*_std_attributes())
        )

        return JsonResponse(results, safe=False)


def search_recommendation_in_category(request, str_match, category):
    if request.method == "GET":
        # filters to category first then searches database name column
        results = get_list_or_404(
            Recommendations.objects.filter(category__iexact=category)
            .filter(name__icontains=str_match)
            .values(*_std_attributes(False))
        )

        return JsonResponse(results, safe=False)
