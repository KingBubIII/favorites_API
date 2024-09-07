from rest_framework import serializers
from Recommendations.models import Recommendations


class RecommendationSerializer(serializers.ModelSerializer):
    """
    This transforms the Recommendation class into a json output so that each class attribute is a key value pair
    Extending the serializer class in order optionally exclude some class attributes

    Keyword arguments:
    non keyword argument:Recommendation instance -- If you want to get each attribute's value in a json format

    Return: JSON in bytestring datatype
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

        if kwargs["exclude_fields"]:
            for field_name in kwargs["exclude_fields"]:
                self.fields.pop(field_name)

    class Meta:
        model = Recommendations
        fields = "__all__"
