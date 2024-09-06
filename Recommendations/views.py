from django.shortcuts import HttpResponse, get_object_or_404, get_list_or_404
from .models import Recommendations
from django.forms.models import model_to_dict
from django.db.models import Subquery
from random import choice
from rest_framework.response import Response
from rest_framework.decorators import api_view


# this is for the values method instead of hard-coding each attribute I need usually
def _std_attributes(category=True):
    """
    This is for the 'values' method instead of hard-coding each attribute I need usually

    Keyword arguments:
    category:str -- Most common use case for this function is split evenly between needing `category` and not

    Return: list of strings, meant to be unpacked with a `*` operator
    """

    attributes = ["id", "name", "comments", "link", "suggester"]
    if category:
        attributes.append("category")

    return attributes


@api_view(["GET"])
def latest(request):
    """
    Gets the last added items to recommendations database, gets multiple items since the time is only specific to a day

    Return: List_Recommendations[Attributes_Dictionary]
    """

    if request.method == "GET":
        subquery_timestamp = Recommendations.objects.order_by("-date_added").values(
            "date_added"
        )[:1]

        most_recent_recommendations = get_list_or_404(
            Recommendations.objects.filter(
                date_added__exact=Subquery(subquery_timestamp)
            ).values(*_std_attributes())
        )

        return Response(most_recent_recommendations)


@api_view(["GET"])
def latest_by_category(request, category):
    """
    Gets the last added items to recommendations database in a specific category, gets multiple items since the time is only specific to a day

    Keyword arguments:
    category:str -- user specified to match category in database

    Return: List_Recommendations[Attributes_Dictionary]
    """

    if request.method == "GET":
        subquery_timestamp = Recommendations.objects.order_by("-date_added").values(
            "date_added"
        )[:1]

        most_recent_recommendations = get_list_or_404(
            Recommendations.objects.filter(category__iexact=category)
            .filter(date_added__exact=Subquery(subquery_timestamp))
            .values(*_std_attributes(False))
        )

        return Response(most_recent_recommendations)


@api_view(["GET"])
def random_recommendation(request):
    """
    Gets a random favorite from database

    Return: Attributes_Dictionary
    """

    if request.method == "GET":
        # gets all ids from Recommendations table without loading other fields
        pks = Recommendations.objects.values_list("pk", flat=True)
        # picks a random id
        random_pk = choice(pks)
        # filters to only the chosen id and puts in a list to get values easier
        random_obj = get_list_or_404(
            Recommendations.objects.filter(pk=random_pk).values(*_std_attributes())
        )[0]

        return Response(random_obj)


@api_view(["GET"])
def random_recommendation_from_category(request, category):
    """
    Gets a random favorite in a certain category from database

    Keyword arguments:
    category:str -- category matching any category in database

    Return: Attributes_Dictionary
    """

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

        return Response(random_obj)


@api_view(["GET"])
def search_recommendation(request, str_match):
    """
    Searches database name column for favorite names containing user search

    Keyword arguments:
    str_match:str -- user specified string, effectively `LIKE "%string%"` in SQL

    Return: List_Recommendations[Attributes_Dictionary]
    """

    if request.method == "GET":
        # searches database name column
        results = get_list_or_404(
            Recommendations.objects.filter(name__icontains=str_match).values(*_std_attributes())
        )

        return Response(results)


@api_view(["GET"])
def search_recommendation_in_category(request, str_match, category):
    """
    Searches database name column in matching categories for favorite names containing user search

    Keyword arguments:
    str_match:str -- user specified string, effectively `LIKE "%string%"` in SQL
    category:str -- category matching any categories in database

    Return: List_Recommendations[Attributes_Dictionary]
    """

    if request.method == "GET":
        # filters to category first then searches database name column
        results = get_list_or_404(
            Recommendations.objects.filter(category__iexact=category)
            .filter(name__icontains=str_match)
            .values(*_std_attributes(False))
        )

        return Response(results)
