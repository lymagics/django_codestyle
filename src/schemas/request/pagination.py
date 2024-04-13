from rest_framework import serializers


class PaginationIn(serializers.Serializer):
    limit = serializers.IntegerField(default=10, min_value=0)
    offset = serializers.IntegerField(default=0, min_value=0)
