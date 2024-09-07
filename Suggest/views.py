from django.shortcuts import HttpResponse, get_object_or_404, get_list_or_404
from Recommendations.models import Recommendations
from django.forms.models import model_to_dict
from django.db.models import Subquery
from random import choice
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Recommendations.views import _std_attributes
from Recommendations.serializer import RecommendationSerializer


@api_view(["POST"])
def suggest(request):
    """
    This allows the user to add something to the recommendation table

    Keyword arguments:
    JSON -- Requires at least 'name' and 'category' keys and can also take 'comments', 'link', and 'suggester' keys

    Return: JSON with the new entry data like 'id' and 'date_added' keys
    """

    if request.method == "POST":
        # get json from request
        new_data = request.data
        # checks for minimum requirements to make a new entry in the recommendations table
        try:
            new_data["name"]
            new_data["category"]
        except KeyError as e:
            # creates a json with details of what was missing from the json in order to create a new database entry
            bad_response = {
                "error_type": "malformed_json",
                "error_description": "JSON data missing 'name' and or 'category' keys",
            }
            # status 400 for invald input json
            return Response(bad_response, status=400)

        # create new instance of Recommendations
        new_rec = Recommendations()

        # gets all field names in order to only add relavant data
        fields = new_rec._meta.get_fields()
        for field in fields:
            field_name = field.name
            # if get a KeyError than the json data didn't include that data and can be set to NULL in the database
            try:
                setattr(new_rec, field_name, new_data[field_name])
            except KeyError as e:
                setattr(new_rec, field_name, None)

        # verifies good data
        new_rec.clean_fields()
        # saves new recommendation in the database
        new_rec.save()

        # serializes the new database entry and returns all fields so that user doesn't have to make a follow up request
        myserializer = RecommendationSerializer(new_rec, exclude_fields=["category"])

        # status 200 for confirmation that the new entry is completed
        return Response(myserializer.data, status=200)
